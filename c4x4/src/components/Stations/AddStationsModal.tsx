import {useState, useContext} from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Modal from "@mui/material/Modal";
import AddStationForm from "./AddStationForm.tsx";
import FormikAddStation from "./FormikAddStation";
import { ActiveSaveContext } from "../../contexts/ActiveSaveProvider.tsx";
import AddCancelButtonPanel from "../Buttons/AddCancelButtonPanel.tsx";

const style = {
  mt: 5,
  position: 'absolute',
  display: 'block',
  maxHeight: '80%',
  overflow: 'auto',
  top: '40%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '60%',
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4
};

export default function AddStationsModal() {
  const activeSave = useContext(ActiveSaveContext)
  const [isOpen, setOpen] = useState(false)
  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  return (
    <>
      <Box display='flex' justifyContent='flex-end'>
        <Button variant="contained" onClick={handleOpen} disabled={Boolean(!activeSave.activeSave.id)}>Add Station</Button>
      </Box>
      <Modal open={isOpen} onClose={handleClose}>
        <Box sx={style}>
          <FormikAddStation cancelAction={handleClose} submitAction={handleClose}/>
        </Box>
      </Modal>
    </>
  )
}