import Modal from "@mui/material/Modal";
import Box from "@mui/material/Box";
import {Typography} from "@mui/material";
import SectorsTable from "./SectorTable.tsx";
import {addOwnedSectors, getSectorTemplates} from "../../functions/responses.ts";
import AddCancelButtonPanel from "../Buttons/AddCancelButtonPanel.tsx";
import {useContext, useState} from "react";
import {ActiveSaveContext} from "../../providers/ActiveSaveProvider.tsx";
import {OwnedSectorsContext} from "./OwnedSectorsProvider.tsx";
import {SelectedSectorsContext} from "./SelectedSectorsProvider.tsx";

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

export default function AddSectorModal({ open, handleClose }) {
  const ownedSectorsContext = useContext(OwnedSectorsContext)
  const selectedSectors = useContext(SelectedSectorsContext)
  const activeSave = useContext(ActiveSaveContext)

  const addSectors = () => {
    const sectors = Array.from(selectedSectors.selectedSectors.ids)
    if (!activeSave.activeSave.id) {
      handleClose()
      return
    }
    addOwnedSectors(activeSave.activeSave.id, sectors).then(() => {
      ownedSectorsContext.setChanged(true)
      handleClose()
    })
  }

  return (
    <Modal open={open} onClose={handleClose}>
      <Box sx={style}>
        <Typography variant="h6">Select Sectors</Typography>
        <SectorsTable getFunction={getSectorTemplates} checkboxSelection/>
        <AddCancelButtonPanel addAction={addSectors} cancelAction={handleClose} />
      </Box>
    </Modal>
  )
};