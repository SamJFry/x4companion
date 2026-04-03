import {ComponentType, SyntheticEvent, useState} from 'react'
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import Grid from "@mui/material/Grid";
import {Typography} from "@mui/material";
import { SxProps, Theme } from "@mui/material/styles";
import {useFormikContext} from "formik";

type FormFieldGridProps<T> = {
  title: string
  fieldsParent: string
  field: ComponentType<T>
  fieldProps: T
  sx?: SxProps<Theme>
}

interface KeyCountOption {
  key?: number
  count?: number
}

export default function FormFieldGrid({ title, fieldsParent, field, fieldProps, sx }: FormFieldGridProps<any>) {
  const FieldComponent = field
  const [fieldCount, setFieldCount] = useState<number>(0)
  const formik = useFormikContext()

  const handleQuantityChange = (index: number, event: SyntheticEvent, currentValue: KeyCountOption[]) => {
    if (currentValue[index] === undefined) {
      currentValue[index] = {count: event.target.value}
    } else {
      currentValue[index].count = event.target.value
    }
  }

  const handleOptionChange = (index: number, value: Record<string, any>, currentValue: KeyCountOption[]) => {
    if (currentValue[index] === undefined) {
      currentValue[index] = {id: value.key}
    } else if (currentValue[index] && !value) {
      delete currentValue[index].id
    } else {
      currentValue[index].id = value.key
    }
  }

  const handleChange = (index: number, event: SyntheticEvent, value?: Record<string, any>) => {
    const currentValue = formik.values[fieldsParent]
    if (value === undefined) {
      handleQuantityChange(index, event, currentValue)
    } else {
      handleOptionChange(index, value, currentValue)
    }
    if (currentValue[index] === undefined && !value) {
      currentValue[index] = {quantity: event.target.value}
    } else if (currentValue[index] === undefined && value) {
      currentValue[index] = {key: value.key}
    }
  }

  const handleDeleteField = () =>{
    formik.values[fieldsParent].pop()
    setFieldCount(fieldCount - 1)
  }

  return <>
    <Grid container spacing={2} sx={sx}>
      <Grid size={{lg: 8}}>
        <Typography fontWeight="bold">{title}</Typography>
      </Grid>
      <Grid size={{lg: 2}}>
      </Grid>
      <Grid size={{lg: 2}}>
        <Box display="flex" justifyContent="flex-end">
          <Button variant="outlined" size="small" onClick={handleDeleteField}>
            <RemoveIcon fontSize="small" />
          </Button>
          <Button sx={{ml: 1}} variant="contained" size="small" onClick={() => setFieldCount(fieldCount + 1)}>
            <AddIcon fontSize="small" />
          </Button>
        </Box>
      </Grid>
      <Grid size={{ lg: 12}}>
        {Array.from({ length: fieldCount }).map((_, index) => (
          <Grid key={index} size={{ lg: 12, xs: 12 }} sx={{mb: 1}}>
            <FieldComponent name={`${fieldProps.name}-${index}`}{...fieldProps} onChange={(e, value) => handleChange(index, e, value)}/>
          </Grid>
        ))}
      </Grid>
    </Grid>
  </>
}