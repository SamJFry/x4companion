import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import SectorsAutoComplete from "../Sectors/SectorsAutoComplete.tsx";
import OwnedSectorsProvider from "../Sectors/OwnedSectorsProvider.tsx";



export default function AddStationForm() {
  return (
    <OwnedSectorsProvider>
      <Box>
        <TextField id="outlined-basic" label="Name" variant="outlined" />
      <SectorsAutoComplete />
      </Box>
    </OwnedSectorsProvider>
  )
}