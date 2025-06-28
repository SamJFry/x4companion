import Box from "@mui/material/Box"
import Button from "@mui/material/Button"
import { ActiveSaveContext } from "../../contexts/ActiveSaveProvider.tsx";
import {useContext, useState } from "react";
import AddSectorModal from "./AddSectorModal.tsx";

export default function AddSectorButton() {
  const activeSave = useContext(ActiveSaveContext)
  const [isOpen, setOpen] = useState(false)
  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  return (
    <>
      <Box display='flex' justifyContent='flex-end'>
        <Button variant="contained" onClick={handleOpen} disabled={Boolean(!activeSave.activeSave.id)}>Add Sector</Button>
      </Box>
      <AddSectorModal open={isOpen} handleClose={() => handleClose()}></AddSectorModal>
    </>
  )
}
