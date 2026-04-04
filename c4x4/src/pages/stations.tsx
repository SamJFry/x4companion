import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import AddStationsModal from "../components/Stations/AddStationsModal.tsx";
import OwnedStationsTable from "../components/Stations/OwnedStationsTable.tsx";
import {Grid} from "@mui/material";

export default function Stations() {
  return (
    <Box sx={{flexGrow: 1, m: '5%'}}>
      <Typography variant="h3">Stations</Typography>
      <Grid container spacing={2} sx={{mb: 2}}>
        <Grid size={{ lg: 8, xs: 12, sm: 8 }}>
          <Typography variant="subtitle1">
            Manage the stations in your Empire.
          </Typography>
        </Grid>
        <Grid size={{ lg: 4, xs: 12, sm: 4 }}>
          <AddStationsModal />
        </Grid>
        <OwnedStationsTable />
      </Grid>
    </Box>
  )
}