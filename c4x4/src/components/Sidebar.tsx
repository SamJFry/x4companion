import {DashboardLayout, ThemeSwitcher} from '@toolpad/core/DashboardLayout';
import ListItemText from '@mui/material/ListItemText';
import ListIcon from '@mui/icons-material/List';
import Popover from '@mui/material/Popover';
import * as React from "react";
import Button from "@mui/material/Button";
import MenuItem from "@mui/material/MenuItem";
import {OnHoverDelete} from "./DeleteButton.tsx";
import {useEffect, useState, useContext} from "react";
import {getSaveGames, deleteSaveGame} from "../functions/responses.ts";
import getCookie, {deleteCookie} from "../functions/cookies.ts";
import {ActiveSaveContext} from "../providers/ActiveSaveProvider.tsx";
import {NewSaveModal} from "./SaveModal.tsx"
import LogOut from "./Logout.tsx";
import {SaveIndicator} from "./SaveIndicator.tsx";
import {Divider, Box} from "@mui/material";
import ListItemIcon from "@mui/material/ListItemIcon";



interface SaveGame {
  id: string
  name: string
  dataset_id: string
}

export default function TopBarActions() {
  const [saves, setSaves] = useState<Array<object>>([])
  const activeSaveContext = useContext(ActiveSaveContext)
  const getSaves = async () => {
    const fetchedSaves = await getSaveGames()
    setSaves(fetchedSaves)
  }
  useEffect(() => {
    getSaveGames().then((data) => setSaves(data))
  }, [])
  const handleClickDelete = async (id: Number) => {
    const cookie = Number(getCookie('saveId'))
    if (id === cookie) {
      deleteCookie('saveId')
    }
    await deleteSaveGame(id)
    await getSaves()
  }
  const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(null);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleSwitchSave = (save: SaveGame) => {
    activeSaveContext.setNewSave(save);
    handleClose()
  }
  const open = Boolean(anchorEl);
  return (
    <>
      <Button variant="outlined" startIcon={<ListIcon />} onClick={handleClick}>
        Saves
      </Button>
      <Popover
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}
      >
        {saves.map((save: object) => (
          <MenuItem  key={save["id"]}>
            <ListItemIcon>
              <OnHoverDelete size="small" onClick={() => handleClickDelete(save["id"])}/>
            </ListItemIcon>
            <Box onClick={() => handleSwitchSave(save)}>
              <ListItemText>{save["name"]}</ListItemText>
            </Box>
          </MenuItem>
        ))}
        <Divider />
        <NewSaveModal createAction={getSaves} />
      </Popover>
      <SaveIndicator saves={saves}/>
      <ThemeSwitcher />
      <LogOut />
    </>
  );
}
