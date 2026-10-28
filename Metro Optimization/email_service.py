import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailService:
    """Service to send email alerts to passengers"""
    
    def __init__(self):
        self.sender_email = os.getenv('EMAIL_ADDRESS', 'metro.optimized@gmail.com')
        self.sender_password = os.getenv('EMAIL_PASSWORD', 'your_app_password_here')
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
    
    def send_journey_summary(self, recipient_email, journey_data):
        """Send journey summary email"""
        subject = "Your Metro Journey Summary"
        
        html_content = f"""
        <html>
            <body style="font-family: 'Arial', sans-serif; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 8px;">
                    <h2 style="color: #003366;">Journey Summary</h2>
                    <p>Dear Passenger,</p>
                    <p>Here's a summary of your recent metro journey:</p>
                    
                    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                        <tr style="background-color: #f0f0f0;">
                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>From</strong></td>
                            <td style="padding: 10px; border: 1px solid #ddd;">{journey_data.get('from_station', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>To</strong></td>
                            <td style="padding: 10px; border: 1px solid #ddd;">{journey_data.get('to_station', 'N/A')}</td>
                        </tr>
                        <tr style="background-color: #f0f0f0;">
                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Distance</strong></td>
                            <td style="padding: 10px; border: 1px solid #ddd;">{journey_data.get('distance', 'N/A')} km</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Fare Paid</strong></td>
                            <td style="padding: 10px; border: 1px solid #ddd;">₹{journey_data.get('fare', 'N/A')}</td>
                        </tr>
                        <tr style="background-color: #f0f0f0;">
                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Time</strong></td>
                            <td style="padding: 10px; border: 1px solid #ddd;">{journey_data.get('time', 'N/A')}</td>
                        </tr>
                    </table>
                    
                    <p>Thank you for using Bangalore Metro!</p>
                    <p style="color: #666; font-size: 12px;">This is an automated message. Please do not reply.</p>
                </div>
            </body>
        </html>
        """
        
        self._send_email(recipient_email, subject, html_content)
    
    def send_line_alert(self, recipient_email, alert_data):
        """Send line status alert email"""
        subject = f"🚨 Metro {alert_data['line_name']} - {alert_data['status']}"
        
        html_content = f"""
        <html>
            <body style="font-family: 'Arial', sans-serif; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 8px;">
                    <h2 style="color: #d32f2f;">⚠️ Service Alert</h2>
                    <p>Dear Passenger,</p>
                    <p style="font-size: 16px; font-weight: bold;">
                        <span style="color: {alert_data['color']};">●</span> {alert_data['line_name']}
                    </p>
                    <p><strong>Status:</strong> <span style="color: #d32f2f; font-weight: bold;">{alert_data['status'].upper()}</span></p>
                    <p><strong>Details:</strong> {alert_data['message']}</p>
                    <p><strong>Expected Resolution:</strong> {alert_data.get('resolution_time', 'To be updated soon')}</p>
                    
                    <p style="color: #666; font-size: 12px;">For live updates, check our website or mobile app.</p>
                </div>
            </body>
        </html>
        """
        
        self._send_email(recipient_email, subject, html_content)
    
    def send_recharge_confirmation(self, recipient_email, transaction_data):
        """Send card recharge confirmation email"""
        subject = "✅ Card Recharge Successful"
        
        html_content = f"""
        <html>
            <body style="font-family: 'Arial', sans-serif; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 8px;">
                    <h2 style="color: #4caf50;">✅ Recharge Successful</h2>
                    <p>Dear Passenger,</p>
                    <p>Your metro card has been successfully recharged!</p>
                    
                    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                        <tr style="background-color: #f0f0f0;">
                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Card Number</strong></td>
                            <td style="padding: 10px; border: 1px solid #ddd;">****{transaction_data['card_last_4']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Amount</strong></td>
                            <td style="padding: 10px; border: 1px solid #ddd;">₹{transaction_data['amount']}</td>
                        </tr>
                        <tr style="background-color: #f0f0f0;">
                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Transaction ID</strong></td>
                            <td style="padding: 10px; border: 1px solid #ddd;">{transaction_data['transaction_id']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border: 1px solid #ddd;"><strong>New Balance</strong></td>
                            <td style="padding: 10px; border: 1px solid #ddd;">₹{transaction_data['new_balance']}</td>
                        </tr>
                    </table>
                    
                    <p style="color: #666; font-size: 12px;">This is an automated message. Please do not reply.</p>
                </div>
            </body>
        </html>
        """
        
        self._send_email(recipient_email, subject, html_content)
    
    def send_kyc_reminder(self, recipient_email, user_name):
        """Send KYC verification reminder email"""
        subject = "⏰ Reminder: Complete Your KYC Verification"
        
        html_content = f"""
        <html>
            <body style="font-family: 'Arial', sans-serif; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 8px;">
                    <h2 style="color: #ff9800;">⏰ KYC Verification Reminder</h2>
                    <p>Dear {user_name},</p>
                    <p>To enjoy unlimited benefits on your metro card, please complete your KYC verification.</p>
                    <p><strong>Benefits of KYC Verification:</strong></p>
                    <ul style="color: #666;">
                        <li>Cashless payments enabled</li>
                        <li>Higher balance limit</li>
                        <li>Travel insurance coverage</li>
                        <li>Exclusive offers and discounts</li>
                    </ul>
                    <p><a href="https://metrooptimized.com/kyc" style="display: inline-block; padding: 10px 20px; background-color: #3b82f6; color: white; text-decoration: none; border-radius: 4px;">Complete KYC Now</a></p>
                    <p style="color: #666; font-size: 12px;">This is an automated message. Please do not reply.</p>
                </div>
            </body>
        </html>
        """
        
        self._send_email(recipient_email, subject, html_content)
    
    def _send_email(self, recipient_email, subject, html_content):
        """Internal method to send email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # For demo purposes, print instead of sending
            # In production, use actual SMTP
            print(f"[EMAIL SENT] To: {recipient_email}")
            print(f"Subject: {subject}")
            print("---")
            
            # Uncomment below for actual email sending:
            # try:
            #     with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            #         server.starttls()
            #         server.login(self.sender_email, self.sender_password)
            #         server.send_message(msg)
            #     return True
            # except Exception as e:
            #     print(f"Failed to send email: {e}")
            #     return False
            
            return True
        except Exception as e:
            print(f"Error preparing email: {e}")
            return False
