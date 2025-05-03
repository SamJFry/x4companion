import Typography from '@mui/material/Typography'
import getCookie, {setCookie} from "../functions/cookies.ts";

interface SaveIndicatorProps {
  saves: Array<object>
}

export function SaveIndicator({ saves }: SaveIndicatorProps) {
  const saveCookie = Number(getCookie('saveId'))
  if (saveCookie && saves.length !== 0) {
    const save = saves.find((element) => element.id === saveCookie)
    setCookie('datasetId', save.dataset_id)
    return <Typography color="primary">Save: {save.name}</Typography>
  }
  if (saves.length !== 0) {
    setCookie('saveId', saves[0].id)
    setCookie('datasetId', saves[0].dataset.id)
    return <Typography color="primary">Save: {saves[0]["name"]}</Typography>
  }
  return <Typography color="primary"> No Saves</Typography>
}