import { Link, Outlet, useLocation } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { useAuth } from "../auth";
import { ProjectProvider } from "../projects/ProjectContext";

export const AppLayout = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const location = useLocation(); // get current route location
  const isProjectsPage = location.pathname.startsWith("/projects"); // check if on projects page

  return (
    <ProjectProvider>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          minHeight: "100vh",
        }}
      >
        {/* Header AppBar */}
        <AppBar
          position="fixed"
          elevation={isProjectsPage ? 0 : 4} // No shadow on projects page, shadow on others

          sx={{ top: 0,
            left: 0,
            right: 0,
            zIndex: 1200,
            backgroundColor: isProjectsPage ? "#ffffff " : undefined,

            color: isProjectsPage ? "#111827" : undefined,
            borderBottom: isProjectsPage ? "1px solid #e5e7eb" : undefined,

          }}
        >
          <Toolbar sx={{ justifyContent: "space-between" }}>
            <Box sx={{ display: "flex", gap: 2 }}>
              {/* Center - Projects page*/}
              {isProjectsPage && (
                <Typography
                variant="h6"
                sx={{
                color: isProjectsPage ? "primary.main" : "inherit",
                fontWeight: isProjectsPage ? 600 : 400,
              }}
            >
              Projects
            </Typography>
          )}
              <Button color="inherit" component={Link} to="/"
              sx ={{ color: isProjectsPage ? "primary.main" : "inherit"}}
              >
                Home
              </Button>
              <Button color="inherit" component={Link} to="/account"
              sx ={{ color: isProjectsPage ? "#374151" : "inherit"}}
              >
                Account
              </Button>
            </Box>

            {/* Center - App Title */}
            {!isProjectsPage && (
            <Typography
              variant="h6"
              sx={{
                position: "absolute",
                left: "50%",
                transform: "translateX(-50%)",
                fontWeight: 600,
              }}
            >
              Hardware Checkout App
            </Typography>
          )}

            {/* Right side - Auth button */}
            <Box>
              {!isAuthenticated ? (
                <Button color="inherit" component={Link} to="/auth"
                sx={{ color: isProjectsPage ? "#374151" : "inherit" }}
                >
                  Sign in
                </Button>
              ) : (
                <Button color="inherit" onClick={logout}>
                  Sign out ({user?.userId})
                </Button>
            )}
            </Box>
          </Toolbar>
        </AppBar>

        {/* Main Content Area */}
        <Container
          component="main"
          sx={{
            flexGrow: 1,
            py: 3,
            mt: 8,
            mb: 8,
          }}
        >
          <Outlet />
        </Container>

        {/* Footer AppBar */}
        <AppBar
          component="footer"
          position="fixed"
          sx={{
            top: "auto",
            bottom: 0,
            backgroundColor: (theme) =>
              theme.palette.mode === "light"
                ? theme.palette.grey[800]
                : theme.palette.grey[900],
          }}
        >
          <Toolbar
            sx={{ justifyContent: "center", minHeight: "48px !important" }}
          >
            <Typography
              variant="body2"
              color="inherit"
              align="center"
              sx={{ opacity: 0.8 }}
            >
              © {new Date().getFullYear()} Cloud Native Team Project. All rights
              reserved.
            </Typography>
          </Toolbar>
        </AppBar>
      </Box>
    </ProjectProvider>
  );
};
