import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import OwnedSectorsTable from "./OwnedSectorsTable.tsx"
import AddSectorModal from "./AddSectorModal.tsx";
import OwnedSectorsProvider from "./OwnedSectorsProvider.tsx";
import SelectedSectorsProvider from "./SelectedSectorsProvider.tsx";
import {Grid} from "@mui/material";

export default function Sectors() {
  return (
    <OwnedSectorsProvider>
      <Box sx={{ flexGrow: 1, m: '5%', }}>
        <Typography variant="h3">Sectors</Typography>
          <Grid container spacing={2}>
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
        <Typography variant="h5">My Sectors</Typography>
        <OwnedSectorsTable />
      </Box>
    </OwnedSectorsProvider>
  )
}