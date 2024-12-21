import {AppProvider, Navigation} from '@toolpad/core/AppProvider';
import { DashboardLayout } from '@toolpad/core/DashboardLayout';
import FlagOutlinedIcon from '@mui/icons-material/FlagOutlined';
import PlaceOutlinedIcon from "@mui/icons-material/PlaceOutlined";
import PrecisionManufacturingOutlinedIcon from '@mui/icons-material/PrecisionManufacturingOutlined';
import FactoryOutlinedIcon from '@mui/icons-material/FactoryOutlined';
import ApartmentOutlinedIcon from '@mui/icons-material/ApartmentOutlined';
import HouseOutlinedIcon from '@mui/icons-material/HouseOutlined';
import LandslideOutlinedIcon from '@mui/icons-material/LandslideOutlined';

const NAVIGATION: Navigation = [
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
    segment: 'factory-modules',
    title: 'Factory Modules',
    icon: <FactoryOutlinedIcon />,
  },
  {
    segment: 'habitats',
    title: 'Habitats',
    icon: <HouseOutlinedIcon />,
  },
  {
    segment: 'habitat-modules',
    title: 'Habitat Modules',
    icon: <ApartmentOutlinedIcon />
  },
  {
    segment: 'resources',
    title: 'Resources',
    icon: <LandslideOutlinedIcon />
  }
]


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
      <DashboardLayout />
    </AppProvider>
  )
}