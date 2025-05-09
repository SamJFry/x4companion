import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import SectorsAutoComplete from "../Sectors/SectorsAutoComplete.tsx";
import OwnedSectorsProvider from "../Sectors/OwnedSectorsProvider.tsx";
import {Typography} from "@mui/material";
import FormFieldGrid from "../FormFields/AutoCompleteGrid.tsx";



export default function AddStationForm() {
  return (
    <OwnedSectorsProvider>
      <Typography variant="h4" sx={{mb: 2}}>Create Station</Typography>
      <Typography fontWeight="bold">Location</Typography>
      <Grid container spacing={2} sx={{mb: 2}}>
        <Grid size={{ lg: 4, xs: 12 }}>
          <TextField id="outlined-basic" label="Name" variant="outlined" fullWidth />
        </Grid>
        <Grid size={{ lg: 4, xs: 12 }}>
          <SectorsAutoComplete />
        </Grid>
      </Grid>
      <FormFieldGrid title="Factory Modules" field={SectorsAutoComplete} sx={{mb: 2}}/>
      <FormFieldGrid title="Habitat Modules" field={SectorsAutoComplete} />
    </OwnedSectorsProvider>
  )
}