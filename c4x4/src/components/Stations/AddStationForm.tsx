import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import SectorsAutoComplete from "../Sectors/SectorsAutoComplete.tsx";



export default function AddStationForm() {
  return (
    <Box>
      <TextField id="outlined-basic" label="Name" variant="outlined" />
      <SectorsAutoComplete />
    </Box>
  )
}