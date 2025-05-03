import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import { getSaveGameSectors, getSectorTemplates } from "../functions/responses.ts";
import SectorsTable from "./SectorTable.tsx"
import AddSectorModal from "./AddSectorModal.tsx";
import OwnedSectorsProvider from "./OwnedSectorsProvider.tsx";
import {Grid} from "@mui/material";
import { createContext, useState } from "react";

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
              <AddSectorModal />
            </Grid>
          </Grid>
        <Typography variant="h5">My Sectors</Typography>
        <SectorsTable getFunction={getSaveGameSectors} sectorCookie="saveId" />
      </Box>
    </OwnedSectorsProvider>
  )
}