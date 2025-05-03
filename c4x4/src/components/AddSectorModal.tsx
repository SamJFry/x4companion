import Modal from "@mui/material/Modal";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Stack from '@mui/material/Stack';
import SectorsTable from "./SectorTable.tsx";
import {getSectorTemplates} from "../functions/responses.ts";
import {Typography} from "@mui/material";

const style = {
  mt: 5,
  position: 'absolute',
  top: '40%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '60%',
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4
};

export default function AddSectorModal() {
  return (
    <>
      <Box display='flex' justifyContent='flex-end'>
        <Button variant="contained">Add Sector</Button>
      </Box>
      <Modal open={false}>
        <Box sx={style}>
          <Typography variant="h6">Select Sectors</Typography>
          <SectorsTable getFunction={getSectorTemplates} sectorCookie="datasetId" checkboxSelection/>
        </Box>
      </Modal>
    </>
  )
}
