import { z } from 'zod';

export const VideoItemSchema = z.object({
  id: z.string(),
  title: z.string(),
  thumbnail: z.string().optional(),
  link: z.string(),
  duration: z.number().optional(),
  viewCount: z.union([z.number(), z.string()]).optional(),
  uploader: z.string().optional(),
  quality_score: z.number().optional(),
});

export const AuthLoginResponseSchema = z.object({
  token: z.string(),
  role: z.string(),
});

export const LmsVideosResponseSchema = z.object({
  topic: z.string(),
  subject: z.string(),
  personalized_for: z.array(z.string()),
  search_queries: z.array(z.string()),
  video_clusters: z.record(z.string(), z.array(VideoItemSchema)),
  videos: z.array(VideoItemSchema),
});

export const GeneratedCourseModuleSchema = z.object({
  title: z.string(),
  description: z.string().optional(),
  search_term: z.string().optional(),
  videos: z.array(VideoItemSchema).optional(),
  module_test: z
    .object({ topic: z.string(), endpoint: z.string() })
    .optional(),
});

export const GeneratedCourseResponseSchema = z.object({
  title: z.string(),
  modules: z.array(GeneratedCourseModuleSchema),
});

export const TestQuestionSchema = z.object({
  id: z.number(),
  type: z.string(),
  question: z.string().optional(),
  options: z.array(z.string()).optional(),
  correct_answer: z.string().optional(),
  task: z.string().optional(),
});

export const GeneratedTestResponseSchema = z.object({
  title: z.string(),
  questions: z.array(TestQuestionSchema),
});

export const CodingProblemSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string(),
  input_format: z.string().optional(),
  output_format: z.string().optional(),
  constraints: z.string().optional(),
  sample_input: z.string().optional(),
  sample_output: z.string().optional(),
  hints: z.array(z.string()).optional(),
});

export const CodingPracticeResponseSchema = z.object({
  problems: z.array(CodingProblemSchema),
});

export const CodingSubmissionResponseSchema = z.object({
  passed: z.boolean().optional(),
  score: z.number().optional(),
  feedback: z.string().optional(),
  improvements: z.array(z.string()).optional(),
});

export const PerformanceHistoryItemSchema = z.object({
  date: z.string(),
  score: z.number(),
  topic: z.string(),
});

export const WeakTopicItemSchema = z.object({
  _id: z.string(),
  avg_score: z.number(),
  attempts: z.number(),
});

export const PerformanceResponseSchema = z.object({
  history: z.array(PerformanceHistoryItemSchema),
  mastery: z.array(z.record(z.string(), z.unknown())),
  weak_topics: z.array(WeakTopicItemSchema),
});

export const StreakResponseSchema = z.object({
  streak: z.number(),
});

export const CompleteModuleResponseSchema = z.object({
  course_title: z.string(),
  module_title: z.string(),
  score: z.number(),
  pass_mark: z.number(),
  passed: z.boolean(),
  next_action: z.string(),
});

export const LegacyResourceItemSchema = z.object({
  name: z.string(),
  url: z.string(),
});

export const LegacyLessonSchema = z.object({
  id: z.string(),
  title: z.string(),
  type: z.enum(['video', 'quiz', 'text', 'pdf']),
  youtube_url: z.string().optional(),
  content: z.string().optional(),
  resources: z.array(LegacyResourceItemSchema).optional(),
  thumbnail: z.string().optional(),
});

export const LegacyModuleSchema = z.object({
  title: z.string(),
  lessons: z.array(LegacyLessonSchema),
});

export const LegacyCourseSchema = z.object({
  _id: z.string().optional(),
  title: z.string(),
  description: z.string().optional(),
  category: z.string().optional(),
  difficulty: z.string().optional(),
  modules: z.array(LegacyModuleSchema),
});

export const LegacyProgressMapSchema = z.record(z.string(), z.boolean());

export const LegacyProgressToggleResponseSchema = z.object({
  is_completed: z.boolean(),
});

export const LegacyQuizResponseSchema = z.object({
  title: z.string(),
  questions: z.array(
    z.object({
      text: z.string(),
      options: z.array(z.object({ text: z.string() })),
    }),
  ),
});

export const LegacyQuizAttemptResponseSchema = z.object({
  score: z.number(),
  total: z.number(),
  percent: z.number(),
});

export const parseOrThrow = <T>(schema: z.ZodSchema<T>, data: unknown, context: string): T => {
  const parsed = schema.safeParse(data);
  if (!parsed.success) {
    throw new Error(`Invalid ${context} response: ${parsed.error.issues.map((i) => i.path.join('.') + ' ' + i.message).join('; ')}`);
  }
  return parsed.data;
};
