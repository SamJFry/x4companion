import {ElementType} from "react";
import TextField, { TextFieldProps } from "@mui/material/TextField";
import {Grid} from "@mui/material";

type QuantityFieldAddonProps = TextFieldProps & {
  field: ElementType;
}

export default function QuantityFieldAddon ({field, ...props}: QuantityFieldAddonProps) {
  const FieldComponent = field
  return (
    <Grid container spacing={0.5}>
      <Grid size={9}>
        <FieldComponent />
      </Grid>
      <Grid size={3}>
        <TextField type="number" {...props} />
      </Grid>
    </Grid>
    )
}