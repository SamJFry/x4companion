import { ComponentType, useState } from 'react'
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import Grid from "@mui/material/Grid";
import {Typography} from "@mui/material";
import { SxProps, Theme } from "@mui/material/styles";
import { FieldArray } from 'formik';

type FormFieldGridProps<T> = {
  title: string
  field: ComponentType<T>
  fieldProps: T
  sx?: SxProps<Theme>
}

export default function FormFieldGrid({ title, field, fieldProps, sx }: FormFieldGridProps<any>) {
  const FieldComponent = field
  const [fieldCount, setFieldCount] = useState<number>(0)

  return <>
    <Grid container spacing={2} sx={sx}>
      <Grid size={{lg: 8}}>
        <Typography fontWeight="bold">{title}</Typography>
      </Grid>
      <Grid size={{lg: 2}}>

      </Grid>
      <Grid size={{lg: 2}}>
        <Box display="flex" justifyContent="flex-end">
          <Button variant="outlined" onClick={() => setFieldCount(fieldCount - 1)}>
            <RemoveIcon fontSize="small" />
          </Button>
          <Button sx={{ml: 1}} variant="contained" onClick={() => setFieldCount(fieldCount + 1)}>
            <AddIcon fontSize="small" />
          </Button>
        </Box>
      </Grid>
      <Grid size={{ lg: 12}}>
        <FieldArray
          name="bob"
          render={() => (
            <>
              {Array.from({ length: fieldCount }).map((_, index) => (
                <Grid key={index} size={{ lg: 12, xs: 12 }} sx={{mb: 1}}>
                  <FieldComponent {...fieldProps} />
                </Grid>
              ))}
            </>
          )}
          />
      </Grid>
    </Grid>
  </>
}