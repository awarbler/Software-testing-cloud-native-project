import { RouterProvider } from "react-router";
import "./App.css";
import { AuthProvider } from "./auth";
import { router } from "./routes";
import { ProjectProvider } from "./projects/ProjectContext";
import { ThemeProvider } from "@mui/material/styles";
import theme from "./styles/theme";

function App() {
  return (

    <AuthProvider>
      <ProjectProvider> 
        <RouterProvider router={router} />
      </ProjectProvider>
    </AuthProvider>
  );
}

export default App;
