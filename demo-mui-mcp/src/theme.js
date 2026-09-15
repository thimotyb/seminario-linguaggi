import { alpha, createTheme } from "@mui/material/styles";

export const appTheme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#67e8f9" },
    secondary: { main: "#a78bfa" },
    background: { default: "#080c18", paper: "#11182a" },
    success: { main: "#34d399" },
    warning: { main: "#fbbf24" },
  },
  shape: { borderRadius: 16 },
  typography: {
    fontFamily: 'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    h3: { fontWeight: 800, letterSpacing: "-0.04em" },
    h6: { fontWeight: 750 },
    button: { fontWeight: 750, textTransform: "none" },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: ({ theme }) => ({
          border: `1px solid ${alpha(theme.palette.common.white, 0.08)}`,
          backgroundImage: `linear-gradient(145deg, ${alpha(theme.palette.common.white, 0.035)}, transparent)`,
        }),
      },
    },
    MuiButton: { defaultProps: { disableElevation: true } },
  },
});

