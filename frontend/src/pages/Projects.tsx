import { useEffect, useState } from "react";
import { Button, Typography, Dialog, DialogTitle, DialogContent, DialogActions, TextField, CircularProgress, Alert, Box } from "@mui/material";
import LogoutIcon from "@mui/icons-material/Logout";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../auth";
import { projectsApi } from "../api/projectsApi";
import type { Project } from "../api/projectsApi";

import ProjectCard from "../projects/ProjectCard";
import "./Projects.css";


// Projects must come from backend
// membership is stored in the database
// assignedUsers lives in mongodb
// joined must be derived from assignedUsers
// localStorage must not be user but for testing it can be used
// useAuth() provides current user info.
// join/leave must call backend endpoints

// backend owns assignedUsers, ownerUserId, project data


//  project page component
export default function Projects() { // Define the Projects page component
    const navigate = useNavigate(); // Hook for navigation
    const { user } = useAuth(); // Get the current user from the authentication context
    //console.log("Logged in user:", user);

    // State
    const [projects, setProjects] = useState<Project[]>([]); // State to hold the list of projects
    const [loading, setLoading] = useState(true); // State to indicate if projects are being loaded
    const [error, setError] = useState<string | null>(null); // State to hold any error that occurs during loading
    const [searchTerm, setSearchTerm] = useState(""); // State to hold the search term for filtering projects   

    const [showCreateForm, setShowCreateForm] = useState(false); // State to control the visibility of the create project form
    const [newProjectId, setNewProjectId] = useState(""); // State to hold the new project ID input
    const [newProjectName, setNewProjectName] = useState(""); // State to hold the new project name input
    const [newDescription, setNewDescription] = useState(""); // State to hold the new project description input

    // load all projects from the backend
    useEffect(() => {
        if (!user?.userId) return; // If there is no user ID, do not attempt to load projects
        //console.log("Calling API with userId:", user.userId);
        async function loadProjects() {
            try {
                setLoading(true); // Set loading state to true before fetching projects
                const res = await projectsApi.list();
                setProjects(res.data);
            } catch (err) {
                console.error("Failed loading projects:", err);
                setError("Failed to load projects.");
            } finally {
                setLoading(false);
            }
        }
        loadProjects(); // call function to load
    }, [user]); // Effect runs when the user changes

    // Join and leave the project using the API wrapper
    // Join project using API wrapper
    async function handleJoin(projectId: string) {
        if (!user?.userId) return; // Guard against undefined user
        await projectsApi.join(projectId, user.userId);
        const res = await projectsApi.list();
        setProjects(res.data);
    }

    // Leave project using API wrapper
    async function handleLeave(projectId: string) {
        if (!user?.userId) return; // Guard against undefined user
        await projectsApi.leave(projectId, user.userId);
        const res = await projectsApi.list();
        setProjects(res.data);
    }

    if (loading) { return <CircularProgress />; }
    if (error) { return <Alert severity="error">{error}</Alert>; }

    // create project using API wrapper

    async function handleCreateProject() {
        if (!user?.userId) return;
        try {
            await projectsApi.create({
                projectId: newProjectId,
                name: newProjectName,
                description: newDescription,
                ownerUserId: user.userId.toLowerCase(),
            });

            // Refresh list
            const res = await projectsApi.list();
            setProjects(res.data);
            // Reset form
            setNewProjectId("");
            setNewProjectName("");
            setNewDescription("");
            setShowCreateForm(false);
        } catch {
            setError("Failed to create project.");
        }
    }

    // search and filter 

    // normalize userId for comparison
    const normalizedUserId = user?.userId?.toLowerCase() ?? ""; // Normalize the user ID for consistent comparison

    // Filter projects by search
    const filteredProjects = projects.filter((project) => {
        const search = searchTerm.toLowerCase();
        return (
            project.projectId.toLowerCase().includes(search) ||
            project.ownerUserId?.toLowerCase().includes(search)
        );
    });


    // Split into two groups
    const memberProjects = filteredProjects.filter((project) =>
        project.assignedUsers?.includes(normalizedUserId)
    );
    const otherProjects = filteredProjects.filter(
        (project) => !project.assignedUsers?.includes(normalizedUserId)
    );

    // render
    if (loading) { return <CircularProgress />; }
    if (error) { return <Alert severity="error">{error}</Alert>; }

    return (
        <Box
            sx={{
                justifyContent: "space-between",
                backgroundColor: (theme) => theme.palette.background.default,
                minHeight: "100vh",
                px: { xs: 2, sm: 4 },
                py: 4,
            }}
        >
            <div className="projects-page">
                {/* Welcome - left aligned above search */}
                <Box sx={{ mb: 2, textAlign: "left" }}>
                    <Typography
                        variant="h4"
                        sx={{
                            fontWeight: 800,
                            color: "text.primary",
                            textAlign: "left"
                        }}
                    >
                        Welcome
                    </Typography>
                    <Typography
                        sx={{
                            fontWeight: 200,
                            color: "primary.main",
                            textAlign: "left"
                        }}
                    >
                        {user?.userId}
                    </Typography>
                </Box>

                <div className="projects-header">
                    <div className="header-center">
                        <input
                            type="text"
                            placeholder="Search by Project ID or Owner"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="project-search"
                        />
                    </div>


                    <div className="header-buttons">
                        <Button
                            variant="contained"
                            color="primary"
                            sx={{
                                textTransform: "none",
                                fontWeight: 500,
                                borderRadius: 1,
                                "&:hover": { backgroundColor: "primary" },
                            }}
                            onClick={() => setShowCreateForm(!showCreateForm)}
                        >
                            New Project
                        </Button>
                    </div>
                </div>

                {/* create form */}
                {showCreateForm && (
                    <div className="create-form">
                        <input
                            placeholder="Project ID"
                            value={newProjectId}
                            onChange={(e) => setNewProjectId(e.target.value)}
                        />

                        <input
                            placeholder="Project Name"
                            value={newProjectName}
                            onChange={(e) => setNewProjectName(e.target.value)}
                        />

                        <input
                            placeholder="Description"
                            value={newDescription}
                            onChange={(e) => setNewDescription(e.target.value)}
                        />

                        <button onClick={handleCreateProject}>
                            Save
                        </button>

                    </div>
                )}

                {/* member projects */}
                {memberProjects.map((project) => (
                    <ProjectCard
                        key={project._id}
                        project={project}
                        isJoined={true}
                        onJoin={handleJoin}
                        onLeave={handleLeave}
                    />
                ))}

                {/* other projects */}
                {otherProjects.map((project) => (
                    <ProjectCard
                        key={project._id}
                        project={project}
                        isJoined={false}
                        onJoin={handleJoin}
                        onLeave={handleLeave}
                    />
                ))}
            </div>
        </Box>
    );
}