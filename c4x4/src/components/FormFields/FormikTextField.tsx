import { useFormikContext } from "formik";
import TextField, {TextFieldProps} from "@mui/material/TextField";

export type FormikTextFieldProps = TextFieldProps & {
  name: string;
}

export default function FormikTextField({name, ...props}: FormikTextFieldProps){
  const formik = useFormikContext();
  return (
    <TextField
      {...formik.getFieldProps("name")}
      error={formik.touched[name]}
      helperText={formik.errors[name]}
      {...props}
    />
  )
}