import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#00897B",
      light: "#26A69A",
      dark: "#004D40",
      contrastText: "#FFFFFF",
    },
    secondary: {
      main: "#00BCD4",
      dark: "#0097A7",
      contrastText: "#FFFFFF",
    },
    background: {
      default: "#F5F5F5",
      paper: "#FFFFFF",
    },
    text: {
      primary: "#212121",
      secondary: "#666666",
    },
    divider: "#BDBDBD",
    success: { main: "#4CAF50" },
    warning: { main: "#FF9800" },
    error: { main: "#F44336" },
    info: { main: "#2196F3" },
  },
});

export default theme;