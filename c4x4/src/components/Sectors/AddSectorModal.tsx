import Modal from "@mui/material/Modal"
import Box from "@mui/material/Box"
import Button from "@mui/material/Button"
import SectorsTable from "./SectorTable.tsx"
import {getSectorTemplates} from "../../functions/responses.ts"
import AddCancelButtonPanel from "../Buttons/AddCancelButtonPanel.tsx"
import { OwnedSectorsContext } from "./OwnedSectorsProvider.tsx"
import { Typography } from "@mui/material"
import { addOwnedSectors } from "../../functions/responses.ts"
import {SelectedSectorsContext} from "./SelectedSectorsProvider.tsx";
import { ActiveSaveContext } from "../../providers/ActiveSaveProvider.tsx";
import {useContext, useState } from "react";


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
  const [isOpen, setOpen] = useState(false)
  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)
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
    <>
      <Box display='flex' justifyContent='flex-end'>
        <Button variant="contained" onClick={handleOpen} disabled={Boolean(!activeSave.activeSave.id)}>Add Sector</Button>
      </Box>
      <Modal open={isOpen} onClose={handleClose}>
        <Box sx={style}>
          <Typography variant="h6">Select Sectors</Typography>
          <SectorsTable getFunction={getSectorTemplates} checkboxSelection/>
          <AddCancelButtonPanel addAction={addSectors} cancelAction={handleClose} />
        </Box>
      </Modal>
    </>
  )
}
