import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import SectorsAutoComplete from "../Sectors/SectorsAutoComplete.tsx";
import OwnedSectorsProvider from "../Sectors/OwnedSectorsProvider.tsx";



export default function AddStationForm() {
  return (
    <OwnedSectorsProvider>
      <Box>
        <Grid container spacing={2}>
          <Grid size={{ lg: 4, xs: 12 }}>
            <TextField id="outlined-basic" label="Name" variant="outlined" fullWidth />
          </Grid>
          <Grid size={{ lg: 4, xs: 12 }}>
            <SectorsAutoComplete />
          </Grid>
        </Grid>
      </Box>
    </OwnedSectorsProvider>
  )
}