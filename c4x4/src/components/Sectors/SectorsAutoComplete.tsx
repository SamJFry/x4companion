import {useEffect, useState, useContext} from "react";
import {ActiveSaveContext} from "../../contexts/ActiveSaveProvider.tsx";
import {getSaveGameSectors} from "../../functions/responses.ts";
import TextField from "@mui/material/TextField";
import {Autocomplete, Divider, Skeleton} from "@mui/material";
import MenuItem from "@mui/material/MenuItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import AddIcon from "@mui/icons-material/Add";
import AddSectorModal from "./AddSectorModal.tsx";
import SelectedSectorsProvider from "./SelectedSectorsProvider.tsx";
import { OwnedSectorsContext } from "./OwnedSectorsProvider.tsx";
import { useFormikContext } from "formik";


function AddNewOwnedSector({ onClick }) {
  return (
    <>
      <Divider sc={{mt: 1}}/>
      <MenuItem onClick={onClick}>
        <ListItemIcon sx={{ml: 0.5}}>
          <AddIcon fontSize="small" />
        </ListItemIcon>
        Add Owned Sector
      </MenuItem>
    </>
  )
}

export default function SectorsAutoComplete() {
  const activeSave = useContext(ActiveSaveContext)
  const ownedSectors = useContext(OwnedSectorsContext)
  const formik = useFormikContext()
  const [loading, setLoading] = useState(true)
  const [sectors, setSectors] = useState<any>([])
  const [isOpen, setOpen] = useState(false)
  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)

  useEffect(() => {
    setLoading(true)
    if (activeSave.activeSave.id) {
      getSaveGameSectors(activeSave.activeSave.id).then((response: Array<object>) => {
        const options = response.map(sector => ({key: sector.id, label: sector.name}))
        const extendedOptions = [...options, {key: 0, label: 'add', isButton: true}]
        setSectors(extendedOptions)
      })
    }
    setLoading(false)
  }, [ownedSectors, activeSave])

  return (
    <SelectedSectorsProvider>
      {loading ? (
        <Skeleton variant="rectangular" />
      ) : (<>
        <Autocomplete
          options={sectors}
          value={formik.values.sector}
          onChange={(_, newValue) => {
            if (newValue?.isButton) {
              handleOpen()
            } else {
              formik.setFieldValue('sector', newValue)
            }
          }}          renderInput={(params) => (
            <TextField
              {...params}
              error={formik.touched.sector && formik.errors.sector}
              helperText={formik.errors.sector}
              label="Choose a sector" />
          )}
          renderOption={(props, option) => {
            if (option?.key === 0) {
              return <AddNewOwnedSector onClick={handleOpen} {...props}>{option.label}</AddNewOwnedSector>;
            }
            return <MenuItem {...props}>{option.label}</MenuItem>;
          }}
        />
        <AddSectorModal open={isOpen} handleClose={handleClose} />
      </>)}
    </SelectedSectorsProvider>
  )
}