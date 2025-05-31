import { ReactElement, useState, cloneElement } from 'react'
import Button from "@mui/material/Button";
import AddIcon from "@mui/icons-material/Add";
import Grid from "@mui/material/Grid";
import {Typography} from "@mui/material";
import { SxProps, Theme } from "@mui/material/styles";

type FormFieldGridProps = {
  title: string
  field: ReactElement
  sx?: SxProps<Theme>
}

export default function FormFieldGrid({ title, field, sx }: FormFieldGridProps) {
  const [fieldCount, setFieldCount] = useState<number>(0)

  return <>
    <Grid container spacing={2} sx={sx}>
      <Grid size={{lg: 2}}>
        <Typography fontWeight="bold">{title}</Typography>
      </Grid>
      <Grid size={{lg: 10}}>
        <Button variant="contained" onClick={() => setFieldCount(fieldCount + 1)}>
          <AddIcon fontSize="small" />
        </Button>
      </Grid>
      {Array.from({ length: fieldCount }).map(() => (
        <Grid size={{ lg: 4, xs: 12 }}>
          {cloneElement(field)}
        </Grid>
      ))}
    </Grid>
  </>
}