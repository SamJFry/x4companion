import {useState, useEffect} from "react";
import {Modal, Box, Typography, FormControl, InputLabel} from "@mui/material";
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from "@mui/material/MenuItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import AddIcon from "@mui/icons-material/Add";
import ListItemText from "@mui/material/ListItemText";
import { getDatasets } from "../responses.ts";


const style = {
  position: 'absolute',
  top: '20%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '70rem',
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
};

export function NewSaveModal() {
  const [isOpen, setOpen] = useState(true)
  const handleOpen = () => setOpen(true)
  const handleClose = () => setOpen(false)
  const [dataset, setDataset] = useState('');
  const handleChange = (event: SelectChangeEvent) => {
    setDataset(event.target.value);
  };
  const [datasets, setDatasets] = useState<Array<object[]>>([])
  useEffect(() => {
    const getData = async () => {
      const data = await getDatasets()
      setDatasets(data)
    }
    getData()
  }, [])
  return (
    <>
      <MenuItem onClick={handleOpen}>
        <ListItemIcon>
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
          <FormControl size="small" sx={{ m: 1, minWidth: 200 }}>
            <InputLabel id="dataset-select">Dataset</InputLabel>
            <Select
              labelId="dataset-select"
              value={dataset}
              label="Dataset"
              onChange={handleChange}
            >
              {datasets.map((data: object) => (
                <MenuItem value={data["id"]}>{data["name"]}</MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
      </Modal>
    </>
  )
}
