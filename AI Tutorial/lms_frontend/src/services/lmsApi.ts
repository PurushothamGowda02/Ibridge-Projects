import axios from 'axios';
import type {
  CodingPracticeResponse,
  CodingSubmissionResponse,
  CompleteModuleResponse,
  GeneratedCourseResponse,
  GeneratedTestResponse,
  LmsVideosResponse,
  PerformanceResponse,
  StreakResponse,
} from './apiTypes';
import {
  CodingPracticeResponseSchema,
  CodingSubmissionResponseSchema,
  CompleteModuleResponseSchema,
  GeneratedCourseResponseSchema,
  GeneratedTestResponseSchema,
  LmsVideosResponseSchema,
  PerformanceResponseSchema,
  StreakResponseSchema,
  parseOrThrow,
} from './schemas';

export const STORAGE_KEYS = {
  aiGeneratedCourse: 'aiGeneratedCourse',
};

const withAuth = () => {
  const token = localStorage.getItem('token');
  return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
};

export const lmsApi = {
  async getVideos(payload: { subject: string; topic: string; personalize?: boolean }): Promise<{ data: LmsVideosResponse }> {
    const response = await axios.post('/api/v1/lms/videos', payload, withAuth());
    return { data: parseOrThrow(LmsVideosResponseSchema, response.data, 'lms videos') };
  },

  async generateCourse(payload: { topic: string }): Promise<{ data: GeneratedCourseResponse }> {
    const response = await axios.post('/api/v1/lms/generate-course', payload, withAuth());
    return { data: parseOrThrow(GeneratedCourseResponseSchema, response.data, 'lms generate-course') };
  },

  async generateTest(payload: { topic: string; difficulty?: string; type?: string }): Promise<{ data: GeneratedTestResponse }> {
    const response = await axios.post('/api/v1/lms/generate-test', payload, withAuth());
    return { data: parseOrThrow(GeneratedTestResponseSchema, response.data, 'lms generate-test') };
  },

  async generateCodingPractice(payload: { subject: string; topic: string; difficulty?: string }): Promise<{ data: CodingPracticeResponse }> {
    const response = await axios.post('/api/v1/lms/generate-coding-practice', payload, withAuth());
    return { data: parseOrThrow(CodingPracticeResponseSchema, response.data, 'lms generate-coding-practice') };
  },

  async submitCoding(payload: {
    subject: string;
    topic: string;
    problem_id: string;
    language: string;
    code: string;
    problem_statement: string;
  }): Promise<{ data: CodingSubmissionResponse }> {
    const response = await axios.post('/api/v1/lms/submit-coding', payload, withAuth());
    return { data: parseOrThrow(CodingSubmissionResponseSchema, response.data, 'lms submit-coding') };
  },

  async getPerformance(): Promise<{ data: PerformanceResponse }> {
    const response = await axios.get('/api/v1/lms/performance', withAuth());
    return { data: parseOrThrow(PerformanceResponseSchema, response.data, 'lms performance') };
  },

  async getStreak(): Promise<{ data: StreakResponse }> {
    const response = await axios.get('/api/v1/lms/streak', withAuth());
    return { data: parseOrThrow(StreakResponseSchema, response.data, 'lms streak') };
  },

  async completeModule(payload: { course_title: string; module_title: string; score: number; pass_mark: number }): Promise<{ data: CompleteModuleResponse }> {
    const response = await axios.post('/api/v1/lms/complete-module', payload, withAuth());
    return { data: parseOrThrow(CompleteModuleResponseSchema, response.data, 'lms complete-module') };
  },

  async submitTestResult(payload: { topic: string; score: number; total: number }): Promise<{ data: { status: string; percentage: number } }> {
    const response = await axios.post('/api/v1/lms/submit-test-result', payload, withAuth());
    return { data: response.data };
  },

  async saveCourse(payload: { course: unknown }): Promise<{ data: { message: string; course_id: string } }> {
    const response = await axios.post('/api/v1/lms/save-course', payload, withAuth());
    return { data: response.data };
  },

  async joinCourse(payload: { course: unknown; pretest: { correct: number; total: number } }): Promise<{ data: { message: string; course_id: string } }> {
    const response = await axios.post('/api/v1/lms/join-course', payload, withAuth());
    return { data: response.data };
  },

  async myCourses(): Promise<{ data: Array<{ id: string; title: string; joined: boolean; progress_percent: number; pretest_percent: number; course: unknown }> }> {
    const response = await axios.get('/api/v1/lms/my-courses', withAuth());
    return { data: response.data };
  },
};
