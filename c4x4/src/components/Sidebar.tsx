import {AppProvider, Navigation} from "@toolpad/core/AppProvider";
import {DashboardLayout, ThemeSwitcher} from '@toolpad/core/DashboardLayout';
import FlagOutlinedIcon from '@mui/icons-material/FlagOutlined';
import PlaceOutlinedIcon from "@mui/icons-material/PlaceOutlined";
import PrecisionManufacturingOutlinedIcon from '@mui/icons-material/PrecisionManufacturingOutlined';
import FactoryOutlinedIcon from '@mui/icons-material/FactoryOutlined';
import ApartmentOutlinedIcon from '@mui/icons-material/ApartmentOutlined';
import HouseOutlinedIcon from '@mui/icons-material/HouseOutlined';
import LandslideOutlinedIcon from '@mui/icons-material/LandslideOutlined';
import AddIcon from '@mui/icons-material/Add';
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListIcon from '@mui/icons-material/List';
import PopupState, {bindMenu, bindTrigger} from "material-ui-popup-state";
import * as React from "react";
import Button from "@mui/material/Button";
import IconButton from '@mui/material/IconButton';
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import {useEffect, useState} from "react";
import {getSaveGames, deleteSaveGame} from "../responses"
import {Divider} from "@mui/material";

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

interface OnHoverDeleteProps {
  size: 'small' | 'large'
  onClick: () => void
}

function OnHoverDelete(props: OnHoverDeleteProps): React.ReactElement {
  const [isHovered, setIsHovered] = useState(false)
  return (
      <IconButton
        color={isHovered ? "error": "default"}
        size={props.size}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        onClick={props.onClick}
      >
        <DeleteOutlinedIcon fontSize={props.size} />
      </IconButton>
  )
}

function TopBarActions() {
  const [saves, setSaves] = useState<Array<object>>([])
  const [deleteAction, setDeleteAction] = useState(true)
  useEffect(() => {
    if (deleteAction) {
      const getSaves = async () => {
        const fetchedSaves = await getSaveGames()
        setSaves(fetchedSaves)
      }
      getSaves()
      setDeleteAction(false)
    }
  }, [])
  const handleClickDelete = async (id: Number) => {
    await deleteSaveGame(id)
    setDeleteAction(true)
  }
  return (
    <PopupState variant="popover" popupId="demo-popup-menu">
      {(popupState) => (
        <React.Fragment>
          <Button variant="outlined" startIcon={<ListIcon />}{...bindTrigger(popupState)}>
            Saves
          </Button>
          <Menu {...bindMenu(popupState)}>
            {saves.map((save: object) => (
              <MenuItem onClick={popupState.close} key={save["id"]}>
                <ListItemText>{save["name"]}</ListItemText>
                <OnHoverDelete size="small" onClick={() => handleClickDelete(save["id"])}/>
              </MenuItem>
            ))}
            <Divider />
            <MenuItem>
              <ListItemIcon>
                <AddIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText>New Save</ListItemText>
            </MenuItem>
          </Menu>
          <ThemeSwitcher />
        </React.Fragment>
      )}
    </PopupState>
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