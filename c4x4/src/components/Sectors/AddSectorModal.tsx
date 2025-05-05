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
import getCookie from "../../functions/cookies.ts"
import {useContext, useState} from "react";


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

  const addSectors = () => {
    let sectors = Array(selectedSectors.selectedSectors.ids)
    addOwnedSectors(Number(getCookie('saveId')), sectors).then(() => {
      ownedSectorsContext.setChanged(true)
      handleClose()
    })
  }

  return (
    <>
      <Box display='flex' justifyContent='flex-end'>
        <Button variant="contained" onClick={handleOpen}>Add Sector</Button>
      </Box>
      <Modal open={isOpen} onClose={handleClose}>
        <Box sx={style}>
          <Typography variant="h6">Select Sectors</Typography>
          <SectorsTable getFunction={getSectorTemplates} sectorCookie="datasetId" checkboxSelection/>
          <AddCancelButtonPanel addAction={addSectors} cancelAction={handleClose} />
        </Box>
      </Modal>
    </>
  )
}
