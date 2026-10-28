export interface AuthLoginRequest {
  email: string;
  password: string;
}

export interface AuthLoginResponse {
  token: string;
  role: string;
}

export interface AuthRegisterRequest {
  name: string;
  email: string;
  password: string;
  role: string;
  mobile: string;
}

export interface VideoItem {
  id: string;
  title: string;
  thumbnail?: string;
  link: string;
  duration?: number;
  viewCount?: number | string;
  uploader?: string;
  quality_score?: number;
}

export interface LmsVideosResponse {
  topic: string;
  subject: string;
  personalized_for: string[];
  search_queries: string[];
  video_clusters: Record<string, VideoItem[]>;
  videos: VideoItem[];
}

export interface GeneratedCourseModule {
  title: string;
  description?: string;
  search_term?: string;
  videos?: VideoItem[];
  module_test?: {
    topic: string;
    endpoint: string;
  };
}

export interface GeneratedCourseResponse {
  title: string;
  modules: GeneratedCourseModule[];
}

export interface TestQuestion {
  id: number;
  type: string;
  question?: string;
  options?: string[];
  correct_answer?: string;
  task?: string;
}

export interface GeneratedTestResponse {
  title: string;
  questions: TestQuestion[];
}

export interface CodingProblem {
  id: string;
  title: string;
  description: string;
  input_format?: string;
  output_format?: string;
  constraints?: string;
  sample_input?: string;
  sample_output?: string;
  hints?: string[];
}

export interface CodingPracticeResponse {
  problems: CodingProblem[];
}

export interface CodingSubmissionResponse {
  passed?: boolean;
  score?: number;
  feedback?: string;
  improvements?: string[];
}

export interface PerformanceHistoryItem {
  date: string;
  score: number;
  topic: string;
}

export interface WeakTopicItem {
  _id: string;
  avg_score: number;
  attempts: number;
}

export interface PerformanceResponse {
  history: PerformanceHistoryItem[];
  mastery: Array<Record<string, unknown>>;
  weak_topics: WeakTopicItem[];
}

export interface StreakResponse {
  streak: number;
}

export interface CompleteModuleResponse {
  course_title: string;
  module_title: string;
  score: number;
  pass_mark: number;
  passed: boolean;
  next_action: string;
}

export interface LegacyQuizResponse {
  title: string;
  questions: Array<{
    text: string;
    options: Array<{ text: string }>;
  }>;
}

export interface LegacyQuizAttemptResponse {
  score: number;
  total: number;
  percent: number;
}

export interface LegacyProgressToggleResponse {
  is_completed: boolean;
}

export interface LegacyResourceItem {
  name: string;
  url: string;
}

export interface LegacyLesson {
  id: string;
  title: string;
  type: 'video' | 'quiz' | 'text' | 'pdf';
  youtube_url?: string;
  content?: string;
  resources?: LegacyResourceItem[];
  thumbnail?: string;
}

export interface LegacyModule {
  title: string;
  lessons: LegacyLesson[];
}

export interface LegacyCourse {
  _id?: string;
  title: string;
  description?: string;
  category?: string;
  difficulty?: string;
  modules: LegacyModule[];
}

export type LegacyProgressMap = Record<string, boolean>;
