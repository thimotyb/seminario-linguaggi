import { useMemo, useState } from "react";
import {
  AddRounded,
  CheckCircleRounded,
  CloudQueueRounded,
  MoreHorizRounded,
  NotificationsNoneRounded,
  SpeedRounded,
  StorageRounded,
  WarningAmberRounded,
} from "@mui/icons-material";
import {
  AppBar,
  Avatar,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  IconButton,
  LinearProgress,
  MenuItem,
  Select,
  Snackbar,
  Stack,
  Switch,
  TextField,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";

const initialServices = [
  { id: 1, name: "Identity API", region: "West Europe", status: "Operational", latency: 42, enabled: true },
  { id: 2, name: "Payment Worker", region: "Italy North", status: "Degraded", latency: 186, enabled: true },
  { id: 3, name: "Document Store", region: "West Europe", status: "Operational", latency: 71, enabled: true },
];

function MetricCard({ icon, label, value, detail, color = "primary.main" }) {
  return (
    <Card>
      <CardContent>
        <Stack direction="row" sx={{ alignItems: "center", justifyContent: "space-between" }}>
          <Avatar sx={{ bgcolor: "action.hover", color }}>{icon}</Avatar>
          <Typography variant="caption" color="text.secondary">Ultimi 5 min</Typography>
        </Stack>
        <Typography variant="h4" sx={{ mt: 2, fontWeight: 800 }}>{value}</Typography>
        <Typography color="text.secondary">{label}</Typography>
        <Typography variant="caption" color={color}>{detail}</Typography>
      </CardContent>
    </Card>
  );
}

export default function App() {
  const [services, setServices] = useState(initialServices);
  const [environment, setEnvironment] = useState("Produzione");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [snackbar, setSnackbar] = useState("");
  const [newName, setNewName] = useState("");

  const activeCount = services.filter((service) => service.enabled).length;
  const averageLatency = useMemo(
    () => Math.round(services.reduce((total, service) => total + service.latency, 0) / services.length),
    [services],
  );

  function toggleService(id) {
    setServices((current) =>
      current.map((service) =>
        service.id === id ? { ...service, enabled: !service.enabled } : service,
      ),
    );
  }

  function addService() {
    const name = newName.trim();
    if (!name) return;
    setServices((current) => [
      ...current,
      { id: Date.now(), name, region: "West Europe", status: "Operational", latency: 58, enabled: true },
    ]);
    setDialogOpen(false);
    setNewName("");
    setSnackbar(`${name} aggiunto al monitoraggio`);
  }

  return (
    <Box sx={{ minHeight: "100vh" }}>
      <AppBar position="sticky" color="transparent" elevation={0} sx={{ backdropFilter: "blur(18px)", borderBottom: 1, borderColor: "divider" }}>
        <Toolbar sx={{ gap: 2 }}>
          <Avatar sx={{ bgcolor: "primary.main", color: "primary.contrastText" }}><CloudQueueRounded /></Avatar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>Cloud Control Center</Typography>
          <Select size="small" value={environment} onChange={(event) => setEnvironment(event.target.value)} sx={{ minWidth: 145 }}>
            <MenuItem value="Produzione">Produzione</MenuItem>
            <MenuItem value="Collaudo">Collaudo</MenuItem>
            <MenuItem value="Sviluppo">Sviluppo</MenuItem>
          </Select>
          <Tooltip title="Notifiche"><IconButton aria-label="Notifiche"><NotificationsNoneRounded /></IconButton></Tooltip>
        </Toolbar>
      </AppBar>

      <Box component="main" sx={{ width: "min(1180px, calc(100% - 32px))", mx: "auto", py: { xs: 4, md: 7 } }}>
        <Stack direction={{ xs: "column", md: "row" }} sx={{ justifyContent: "space-between", alignItems: { md: "end" }, gap: 3 }}>
          <Box>
            <Chip label={`${environment} · aggiornato ora`} color="primary" variant="outlined" size="small" />
            <Typography variant="h3" sx={{ mt: 2 }}>Stato dei servizi</Typography>
            <Typography color="text.secondary" sx={{ mt: 1 }}>Una dashboard MUI costruita con l'aiuto della documentazione MCP.</Typography>
          </Box>
          <Button aria-label="Aggiungi servizio" variant="contained" startIcon={<AddRounded />} onClick={() => setDialogOpen(true)}>Aggiungi servizio</Button>
        </Stack>

        <Box sx={{ display: "grid", gridTemplateColumns: { xs: "1fr", sm: "repeat(2, 1fr)", lg: "repeat(4, 1fr)" }, gap: 2, mt: 4 }}>
          <MetricCard icon={<CheckCircleRounded />} label="Servizi attivi" value={`${activeCount}/${services.length}`} detail="Configurazione corrente" color="success.main" />
          <MetricCard icon={<SpeedRounded />} label="Latenza media" value={`${averageLatency} ms`} detail="+8 ms rispetto a ieri" color="warning.main" />
          <MetricCard icon={<StorageRounded />} label="Dati elaborati" value="2,4 TB" detail="73% della quota mensile" />
          <MetricCard icon={<WarningAmberRounded />} label="Avvisi aperti" value="1" detail="Payment Worker degradato" color="warning.main" />
        </Box>

        <Card sx={{ mt: 3 }}>
          <CardContent sx={{ p: { xs: 2, md: 3 } }}>
            <Stack direction="row" sx={{ justifyContent: "space-between", alignItems: "center" }}>
              <Box><Typography variant="h6">Servizi monitorati</Typography><Typography variant="body2" color="text.secondary">Attiva o sospendi il monitoraggio.</Typography></Box>
              <IconButton aria-label="Altre opzioni"><MoreHorizRounded /></IconButton>
            </Stack>
            <Divider sx={{ my: 2 }} />
            <Stack divider={<Divider flexItem />}>
              {services.map((service) => (
                <Stack key={service.id} direction={{ xs: "column", sm: "row" }} sx={{ alignItems: { sm: "center" }, gap: 2, py: 2 }}>
                  <Avatar sx={{ bgcolor: service.status === "Operational" ? "success.main" : "warning.main", width: 10, height: 10 }} />
                  <Box sx={{ flexGrow: 1 }}><Typography fontWeight={750}>{service.name}</Typography><Typography variant="body2" color="text.secondary">{service.region}</Typography></Box>
                  <Box sx={{ width: { xs: "100%", sm: 180 } }}><Stack direction="row" sx={{ justifyContent: "space-between" }}><Typography variant="caption">Latenza</Typography><Typography variant="caption">{service.latency} ms</Typography></Stack><LinearProgress variant="determinate" value={Math.min(service.latency / 2.2, 100)} color={service.latency > 150 ? "warning" : "primary"} sx={{ mt: 0.75, height: 6, borderRadius: 99 }} /></Box>
                  <Chip label={service.status === "Operational" ? "Operativo" : "Degradato"} color={service.status === "Operational" ? "success" : "warning"} size="small" variant="outlined" />
                  <Switch checked={service.enabled} onChange={() => toggleService(service.id)} slotProps={{ input: { "aria-label": `Monitoraggio ${service.name}` } }} />
                </Stack>
              ))}
            </Stack>
          </CardContent>
        </Card>
      </Box>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} fullWidth maxWidth="xs">
        <DialogTitle>Nuovo servizio</DialogTitle>
        <DialogContent><TextField autoFocus fullWidth label="Nome del servizio" value={newName} onChange={(event) => setNewName(event.target.value)} onKeyDown={(event) => event.key === "Enter" && addService()} sx={{ mt: 1 }} /></DialogContent>
        <DialogActions><Button onClick={() => setDialogOpen(false)}>Annulla</Button><Button variant="contained" onClick={addService} disabled={!newName.trim()}>Aggiungi</Button></DialogActions>
      </Dialog>
      <Snackbar open={Boolean(snackbar)} autoHideDuration={3500} onClose={() => setSnackbar("")} message={snackbar} />
    </Box>
  );
}
