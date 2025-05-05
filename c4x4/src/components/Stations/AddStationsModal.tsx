import {useState, useContext} from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Modal from "@mui/material/Modal";
import {Typography} from "@mui/material";
import AddStationForm from "./AddStationForm.tsx";
import { ActiveSaveContext } from "../../providers/ActiveSaveProvider.tsx";
import AddCancelButtonPanel from "../Buttons/AddCancelButtonPanel.tsx";

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

export default function AddStationsModal() {
  const [isOpen, setOpen] = useState(false)
  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)
  const activeSave = useContext(ActiveSaveContext)

  return (
    <>
      <Box display='flex' justifyContent='flex-end'>
        <Button variant="contained" onClick={handleOpen} disabled={Boolean(!activeSave.activeSave.id)}>Add Station</Button>
      </Box>
      <Modal open={isOpen} onClose={handleClose}>
        <Box sx={style}>
          <Typography variant="h6" sx={{mb: 2}}>Create Station</Typography>
          <AddStationForm />
          <AddCancelButtonPanel addAction={handleClose} cancelAction={handleClose} />
        </Box>
      </Modal>
    </>
  )
}