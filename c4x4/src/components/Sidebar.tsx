import {AppProvider, Navigation} from "@toolpad/core/AppProvider";
import {DashboardLayout, ThemeSwitcher} from '@toolpad/core/DashboardLayout';
import FlagOutlinedIcon from '@mui/icons-material/FlagOutlined';
import PlaceOutlinedIcon from "@mui/icons-material/PlaceOutlined";
import PrecisionManufacturingOutlinedIcon from '@mui/icons-material/PrecisionManufacturingOutlined';
import FactoryOutlinedIcon from '@mui/icons-material/FactoryOutlined';
import ApartmentOutlinedIcon from '@mui/icons-material/ApartmentOutlined';
import HouseOutlinedIcon from '@mui/icons-material/HouseOutlined';
import LandslideOutlinedIcon from '@mui/icons-material/LandslideOutlined';
import ListItemText from '@mui/material/ListItemText';
import ListIcon from '@mui/icons-material/List';
import Popover from '@mui/material/Popover';
import * as React from "react";
import Button from "@mui/material/Button";
import MenuItem from "@mui/material/MenuItem";
import {OnHoverDelete} from "./DeleteButton.tsx";
import {useEffect, useState} from "react";
import {getSaveGames, deleteSaveGame} from "../functions/responses.ts";
import getCookie, {deleteCookie, setCookie} from "../functions/cookies.ts";
import {NewSaveModal} from "./SaveModal.tsx"
import LogOut from "./Logout.tsx";
import {SaveIndicator} from "./SaveIndicator.tsx";
import {Divider, Box} from "@mui/material";
import ListItemIcon from "@mui/material/ListItemIcon";

const NAVIGATION: Navigation = [
  {kind: 'divider'},

  {
    kind: 'header',
    title: 'Empire',
  },
  {
    segment: 'sectors',
    title: 'Sectors',
    icon: <FlagOutlinedIcon />
  },
  {
    segment: 'stations',
    title: 'Stations',
    icon: <PlaceOutlinedIcon />
  },
  {
    segment: 'factories',
    title: 'Factories',
    icon: <PrecisionManufacturingOutlinedIcon />
  },
  {
    segment: 'habitats',
    title: 'Habitats',
    icon: <HouseOutlinedIcon />,
  },
  {kind: 'divider'},

  {
    kind: 'header',
    title: 'Available Modules',
  },

  {
    segment: 'factory-modules',
    title: 'Factory Modules',
    icon: <FactoryOutlinedIcon />,
  },
  {
    segment: 'habitat-modules',
    title: 'Habitat Modules',
    icon: <ApartmentOutlinedIcon />
  },
  {kind: 'divider'},
  {
    kind: 'header',
    title: 'Other',
  },
  {
    segment: 'resources',
    title: 'Resources',
    icon: <LandslideOutlinedIcon />
  },
  {kind: 'divider'},
]

function TopBarActions() {
  const [saves, setSaves] = useState<Array<object>>([])
  const getSaves = async () => {
    const fetchedSaves = await getSaveGames()
    setSaves(fetchedSaves)
  }
  useEffect(() => {
    getSaves()
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

  const handleSwitchSave = (saveId: Number) => {
    setCookie('saveId', saveId)
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
            <Box onClick={() => handleSwitchSave(save["id"])}>
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

export default function X4Base() {
  return (
    <AppProvider
      navigation={NAVIGATION}
      branding={{
        logo: <img src="/src/assets/X4.svg" alt="x4 logo"/>,
        title: 'Companion',
        homeUrl: '',
      }}
    >
      <DashboardLayout
        slots={{
          toolbarActions: TopBarActions
        }}
      ></DashboardLayout>
    </AppProvider>
  )
}