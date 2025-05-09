import {useEffect, useState, useContext} from "react";
import {ActiveSaveContext} from "../../providers/ActiveSaveProvider.tsx";
import {getSaveGameSectors} from "../../functions/responses.ts";
import TextField from "@mui/material/TextField";
import {Autocomplete, Divider} from "@mui/material";
import MenuItem from "@mui/material/MenuItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import AddIcon from "@mui/icons-material/Add";
import ListItemText from "@mui/material/ListItemText";
import AddSectorModal from "./AddSectorModal.tsx";
import SelectedSectorsProvider from "./SelectedSectorsProvider.tsx";
import OwnedSectorsProvider, {OwnedSectorsContext} from "./OwnedSectorsProvider.tsx";

function AddNewOwnedSector() {
  const [isOpen, setOpen] = useState(false)
  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  return (
    <SelectedSectorsProvider>
      <Divider sc={{mt: 1}}/>
      <MenuItem onClick={handleOpen}>
        <ListItemIcon sx={{ml: 0.5}}>
          <AddIcon fontSize="small" />
        </ListItemIcon>
        Add Owned Sector
      </MenuItem>
      <AddSectorModal open={isOpen} handleClose={handleClose} />
    </SelectedSectorsProvider>
  )
}

export default function SectorsAutoComplete() {
  const activeSave = useContext(ActiveSaveContext);
  const ownedSectors = useContext(OwnedSectorsContext);
  const [loading, setLoading] = useState(true)
  const [sectors, setSectors] = useState<any>([])

  useEffect(() => {
    setLoading(true)
    getSaveGameSectors(activeSave.activeSave.id).then((response: Array<object>) => {
      const options = response.map(sector => ({key: sector.id, label: sector.name}))
      const extendedOptions = [...options, {key: 0, label: 'add', isButton: true}]
      setSectors(extendedOptions)
      setLoading(false)
    })
  }, [ownedSectors]);

  return (
    <Autocomplete
      options={sectors}
      sx={{width: 300}}
      renderInput={(params) => <TextField {...params} label="Choose a sector" />}
      renderOption={(props, option) => {
        if (option?.key === 0) {
          return <AddNewOwnedSector />
        }
        return <MenuItem {...props}>{option.label}</MenuItem>
      }}
    />
  )
}