import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import OwnedSectorsTable from "../components/Sectors/OwnedSectorsTable.tsx"
import AddSectorModal from "../components/Sectors/AddSectorModal.tsx";
import OwnedSectorsProvider from "../components/Sectors/OwnedSectorsProvider.tsx";
import SelectedSectorsProvider from "../components/Sectors/SelectedSectorsProvider.tsx";
import {Grid} from "@mui/material";

export default function Sectors() {
  return (
    <OwnedSectorsProvider>
      <Box sx={{ flexGrow: 1, m: '5%', }}>
        <Typography variant="h3">Sectors</Typography>
        <Grid container spacing={2} sx={{mb: 2}}>
          <Grid size={{ lg: 8, xs: 12, sm: 8 }}>
            <Typography variant="subtitle1">
              Manage the sectors that your empire has a presence in.
            </Typography>
          </Grid>
          <Grid size={{ lg: 4, xs: 12, sm: 4 }}>
            <SelectedSectorsProvider>
              <AddSectorModal />
            </SelectedSectorsProvider>
          </Grid>
        </Grid>
        <OwnedSectorsTable />
      </Box>
    </OwnedSectorsProvider>
  )
}