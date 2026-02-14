import { Card, CardContent, Button, Typography } from "@mui/material";
import type { Project } from "../api/projectsApi";
import "./ProjectCard.css";
import HardwareSetRow from "./HardwareSetRow";


type ProjectCardProps = {
    project: Project;
    isJoined: boolean;
    onJoin?: (projectId: string) => void;
    onLeave?: (projectId: string) => void;
};

export function ProjectCard({ project, isJoined, onJoin, onLeave }: ProjectCardProps) {
    return (
        <Card variant="outlined"
            className={`project-card ${isJoined ? 'joined' : ''}`}>
            <CardContent>
                <div className="project-row">

                    <div className="project-left"> {/* left column container */}

                        <div className="project-title-row"> {/* name + users in one row */}
                            <div className="project-name">{project.name}</div> {/* project name */}
                            {/* Show projectId clearly */}
                            <div className="project-id">
                                ID: {project.projectId}
                            </div>
                            <div className="project-users">{project.assignedUsers?.join(",")}</div> {/* users list */}
                        </div>
                    </div>
                    <div className="project-middle">
                        {/* Example hardware sets — replace later with real data */}
                        <HardwareSetRow label="HWSet1: 40/100" isJoined={isJoined} />
                        <HardwareSetRow label="HWSet2: 0/100" isJoined={isJoined} />
                    </div>

                    <div className="project-right">
                        {isJoined ? (
                            <Button
                                className="join-btn"
                                variant="contained"
                                sx={{
                                backgroundColor: "#0097A7",
                                    "&:hover": { backgroundColor: "#007c91" },
                                }}
                                onClick={() => onLeave?.(project._id)}>
                                Leave
                            </Button>
                        ) : (
                            <Button
                                className="join-btn"
                                variant="contained"
                                sx={{
                                    backgroundColor: "primary.main",
                                    "&:hover": { backgroundColor: "primary.dark" },
                                }}

                                onClick={() => onJoin?.(project._id)}
                            >
                                Join
                            </Button>
                        )}
                    </div>
                </div>
            </CardContent>
    </Card>
    );
}

export default ProjectCard;
