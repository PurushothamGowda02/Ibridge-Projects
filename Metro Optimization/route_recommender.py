from database import db, Station, Fare, MetroLine, TrainSchedule, Journey
from datetime import datetime, timedelta
import math

class RouteRecommender:
    """Smart route recommendation engine for passengers"""
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """Calculate distance between two coordinates using Haversine formula"""
        R = 6371  # Earth's radius in kilometers
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    @staticmethod
    def find_shortest_route(from_station_id, to_station_id):
        """Find shortest route between two stations"""
        from_station = Station.query.get(from_station_id)
        to_station = Station.query.get(to_station_id)
        
        if not from_station or not to_station:
            return None
        
        # Check if stations are on the same line
        if from_station.line_id == to_station.line_id:
            # Same line - direct route
            return {
                'type': 'Direct',
                'lines': [from_station.line.name],
                'from': from_station.name,
                'to': to_station.name,
                'stations': RouteRecommender._get_stations_between(from_station_id, to_station_id),
                'distance': abs(to_station.distance_from_first - from_station.distance_from_first),
                'duration_estimate': RouteRecommender._estimate_duration(
                    from_station.distance_from_first,
                    to_station.distance_from_first
                ),
                'fare': RouteRecommender._calculate_fare(from_station_id, to_station_id)
            }
        
        # Different lines - find interchange stations
        interchange_routes = RouteRecommender._find_interchange_routes(from_station_id, to_station_id)
        
        if interchange_routes:
            best_route = min(interchange_routes, key=lambda x: x['distance'])
            return best_route
        
        return None
    
    @staticmethod
    def _get_stations_between(from_id, to_id):
        """Get all stations between two given stations"""
        from_station = Station.query.get(from_id)
        to_station = Station.query.get(to_id)
        
        if from_station.line_id != to_station.line_id:
            return []
        
        # Ensure proper ordering
        if from_station.order_on_line > to_station.order_on_line:
            from_station, to_station = to_station, from_station
        
        stations = Station.query.filter(
            Station.line_id == from_station.line_id,
            Station.order_on_line >= from_station.order_on_line,
            Station.order_on_line <= to_station.order_on_line
        ).order_by(Station.order_on_line).all()
        
        return [{'name': s.name, 'distance': s.distance_from_first} for s in stations]
    
    @staticmethod
    def _find_interchange_routes(from_id, to_id):
        """Find routes with one interchange"""
        from_station = Station.query.get(from_id)
        to_station = Station.query.get(to_id)
        
        interchange_routes = []
        
        # Get all stations
        all_stations = Station.query.all()
        
        # Find common line stations
        for interchange_station in all_stations:
            if (interchange_station.line_id == from_station.line_id or 
                interchange_station.line_id == to_station.line_id):
                
                # Check if can form a valid route
                if (interchange_station.line_id != from_station.line_id and 
                    interchange_station.line_id == to_station.line_id):
                    
                    dist1 = abs(interchange_station.distance_from_first - from_station.distance_from_first)
                    dist2 = abs(to_station.distance_from_first - interchange_station.distance_from_first)
                    
                    route = {
                        'type': 'Interchange',
                        'lines': [from_station.line.name, to_station.line.name],
                        'from': from_station.name,
                        'interchange': interchange_station.name,
                        'to': to_station.name,
                        'distance': dist1 + dist2,
                        'duration_estimate': RouteRecommender._estimate_duration(dist1, dist2),
                        'fare': RouteRecommender._calculate_fare(from_id, to_id)
                    }
                    interchange_routes.append(route)
        
        return interchange_routes
    
    @staticmethod
    def _estimate_duration(dist1, dist2=0):
        """Estimate journey duration in minutes"""
        # Average speed: 30 km/h, add 2 mins per station
        distance = dist1 + dist2
        travel_time = (distance / 30) * 60  # Convert to minutes
        return int(travel_time) + 5  # Add buffer
    
    @staticmethod
    def _calculate_fare(from_id, to_id):
        """Calculate fare based on number of stations between source and destination"""
        from_station = Station.query.get(from_id)
        to_station = Station.query.get(to_id)
        if not from_station or not to_station:
            return 10

        if from_station.line_id == to_station.line_id:
            station_count = abs(from_station.order_on_line - to_station.order_on_line)
        else:
            # Cross-line: sum of hops as approximation
            station_count = from_station.order_on_line + to_station.order_on_line

        # Bangalore Metro station-slab fare
        if station_count <= 2:
            return 10
        elif station_count <= 4:
            return 20
        elif station_count <= 6:
            return 30
        elif station_count <= 9:
            return 40
        else:
            return 50
    
    @staticmethod
    def get_available_schedules(from_station_id, to_station_id, travel_date=None):
        """Get available train schedules for a route"""
        if not travel_date:
            travel_date = datetime.now()
        
        from_station = Station.query.get(from_station_id)
        to_station = Station.query.get(to_station_id)
        
        if not from_station or not to_station:
            return []
        
        # Get schedules for the line
        line_id = from_station.line_id
        schedules = TrainSchedule.query.filter(
            TrainSchedule.line_id == line_id,
            TrainSchedule.departure_time >= travel_date
        ).order_by(TrainSchedule.departure_time).limit(10).all()
        
        return [{
            'departure': s.departure_time.strftime('%H:%M'),
            'arrival': s.arrival_time.strftime('%H:%M'),
            'capacity': s.train_capacity,
            'available_seats': s.train_capacity - s.current_passengers,
            'crowding': 'High' if s.current_passengers > s.train_capacity * 0.7 else 
                       'Medium' if s.current_passengers > s.train_capacity * 0.4 else 'Low'
        } for s in schedules]
    
    @staticmethod
    def get_personalized_routes(user_id):
        """Get frequently used routes for a passenger (for quick access)"""
        journeys = Journey.query.filter_by(user_id=user_id).order_by(
            Journey.journey_date.desc()
        ).limit(10).all()
        
        route_counts = {}
        for journey in journeys:
            route_key = f"{journey.from_station_id}-{journey.to_station_id}"
            route_counts[route_key] = route_counts.get(route_key, 0) + 1
        
        frequent_routes = []
        for route_key, count in sorted(route_counts.items(), key=lambda x: x[1], reverse=True):
            if count >= 2:  # Show routes used at least twice
                from_id, to_id = map(int, route_key.split('-'))
                from_station = Station.query.get(from_id)
                to_station = Station.query.get(to_id)
                
                if from_station and to_station:
                    frequent_routes.append({
                        'from_station_id': from_id,
                        'to_station_id': to_id,
                        'from': from_station.name,
                        'to': to_station.name,
                        'frequency': count,
                        'last_used': journeys[0].journey_date.strftime('%Y-%m-%d %H:%M')
                    })
        
        return frequent_routes
