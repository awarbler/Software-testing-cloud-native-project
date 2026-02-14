import { api } from "./http";

export type Project = {
    _id: string; // MongoDB id
    projectId: string; // required project id
    name: string; // required name
    description: string; // required description
    ownerUserId?: string; // optional owner user id
    assignedUsers?: string[]; // optional array of assigned user ids
};

// Centralized API wrapper for projects endpoints
export const projectsApi = {

  // GET /api/projects
  list: () =>
    api.get<Project[]>("/projects"),

  // POST /api/projects/:id/join
  join: (projectId: string, userId: string) =>
    api.post(`/projects/${projectId}/join`, { userId }),

  // POST /api/projects/:id/leave
  leave: (projectId: string, userId: string) =>
    api.post(`/projects/${projectId}/leave`, { userId }),

  // POST /api/projects
  create: (project: {
    projectId: string;
    name: string;
    description: string;
    ownerUserId?: string;
  }) =>
    api.post<Project>("/projects", project),
};
