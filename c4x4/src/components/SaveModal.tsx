import {useState, useEffect, ChangeEvent} from "react";
import {Modal, Box, Typography, FormControl, InputLabel} from "@mui/material";
import Select, { SelectChangeEvent } from '@mui/material/Select';
import Button from "@mui/material/Button";
import TextField from '@mui/material/TextField';
import MenuItem from "@mui/material/MenuItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import AddIcon from "@mui/icons-material/Add";
import ListItemText from "@mui/material/ListItemText";
import { getDatasets, createSaveGame } from "../functions/responses.ts";


const style = {
  position: 'absolute',
  top: '20%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '60%',
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4
};

interface ActionProp {
  action: () => void;
}

interface DatasetFormProps {
  cancelAction: () => void;
  createAction: () => void;
}

interface NewSaveModalProps {
  createAction: () => void;
}

export function NewSaveModal({ createAction }: NewSaveModalProps): JSX.Element {
  const [isOpen, setOpen] = useState(false)
  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)
  return (
    <>
      <MenuItem onClick={handleOpen}>
        <ListItemIcon sx={{ml: 0.5}}>
          <AddIcon fontSize="small" />
        </ListItemIcon>
        <ListItemText>New Save</ListItemText>
      </MenuItem>
      <Modal
        open={isOpen}
        onClose={handleClose}
      >
        <Box sx={style}>
          <Typography id="modal-modal-title" variant="h6" component="h2">
            Create New Save
          </Typography>
          <DatasetForm cancelAction={handleClose} createAction={createAction} />
        </Box>
      </Modal>
    </>
  )
}

function DatasetForm({ cancelAction, createAction }: DatasetFormProps) {
  const [dataset, setDataset] = useState('');
  const handleDatasetChange = (event: SelectChangeEvent) => {
    setDataset(event.target.value);
  };
  const [name, setName] = useState('');
  const handleNameChange = (event: ChangeEvent<HTMLInputElement>) => {
    setName(event.target.value)
  }
  const [datasets, setDatasets] = useState<Array<object[]>>([])
  useEffect(() => {
    const getData = async () => {
      const data = await getDatasets()
      setDatasets(data)
    }
    getData()
  }, [])
  const handleCreate = async () => {
    if (!name || !dataset) {
      return
    }
    await createSaveGame(name, Number(dataset))
    createAction()
    cancelAction()
  }
  return (
    <>
      <FormControl sx={{ m: 1, minWidth: '100%' }}>
        <TextField
          id="save-name"
          variant="outlined"
          label="Save Name"
          type="text"
          required
          size="small"
          onChange={handleNameChange}
        />
      </FormControl>
      <FormControl required size="small" sx={{ m: 1, minWidth: '100%' }}>
        <InputLabel className="left-0" id="dataset-select">Dataset</InputLabel>
        <Select
          labelId="dataset-select"
          value={dataset}
          label="Dataset *"
          onChange={handleDatasetChange}
        >
          {datasets.map((data: object) => (
            <MenuItem value={data["id"]}>{data["name"]}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
        <CancelButton action={cancelAction} />
        <CreateButton action={handleCreate} />
      </Box>
    </>
  )
}

function CancelButton({ action }: ActionProp) {
  return (
    <Button onClick={action} variant="outlined" sx={{ m: 0.5 }}>Cancel</Button>
  )
}

function CreateButton({ action }: ActionProp) {
  return (
    <Button onClick={action} variant="contained" sx={{ m: 0.5 }}>Create</Button>
  )
}