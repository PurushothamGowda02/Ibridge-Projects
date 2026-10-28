import axios from 'axios';
import type {
  LegacyCourse,
  LegacyProgressMap,
  LegacyProgressToggleResponse,
  LegacyQuizAttemptResponse,
  LegacyQuizResponse,
} from './apiTypes';
import {
  LegacyCourseSchema,
  LegacyProgressMapSchema,
  LegacyProgressToggleResponseSchema,
  LegacyQuizAttemptResponseSchema,
  LegacyQuizResponseSchema,
  parseOrThrow,
} from './schemas';

export const legacyApi = {
  async getCourseById(courseId: string): Promise<{ data: LegacyCourse }> {
    const response = await axios.get(`/api/v1/courses/${courseId}`);
    return { data: parseOrThrow(LegacyCourseSchema, response.data, 'legacy getCourseById') };
  },

  async getProgress(courseId: string): Promise<{ data: LegacyProgressMap }> {
    const response = await axios.get(`/api/v1/progress/${courseId}`);
    return { data: parseOrThrow(LegacyProgressMapSchema, response.data, 'legacy getProgress') };
  },

  async toggleLessonProgress(lessonId: string, courseId: string): Promise<{ data: LegacyProgressToggleResponse }> {
    const response = await axios.patch(`/api/v1/progress/${lessonId}?course_id=${courseId}`);
    return { data: parseOrThrow(LegacyProgressToggleResponseSchema, response.data, 'legacy toggleLessonProgress') };
  },

  async getQuiz(lessonId: string): Promise<{ data: LegacyQuizResponse }> {
    const response = await axios.get(`/api/v1/quizzes/${lessonId}`);
    return { data: parseOrThrow(LegacyQuizResponseSchema, response.data, 'legacy getQuiz') };
  },

  async submitQuizAttempt(payload: { lesson_id: string; course_id: string; answers: Record<number, number> }): Promise<{ data: LegacyQuizAttemptResponse }> {
    const response = await axios.post('/api/v1/quizzes/attempt', payload);
    return { data: parseOrThrow(LegacyQuizAttemptResponseSchema, response.data, 'legacy submitQuizAttempt') };
  },

  async generateAiCourse(payload: { topic: string; difficulty: string }): Promise<{ data: LegacyCourse }> {
    const response = await axios.post('/api/v1/ai/generate', payload);
    return { data: parseOrThrow(LegacyCourseSchema, response.data, 'legacy generateAiCourse') };
  },

  async createCourse(payload: LegacyCourse): Promise<{ data: unknown }> {
    const response = await axios.post('/api/v1/courses/', payload);
    return { data: response.data };
  },
};
