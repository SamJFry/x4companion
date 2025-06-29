import { Formik } from "formik";
import AddStationForm from "./AddStationForm";
import * as yup from 'yup';

export default function FormikAddStation({ cancelAction, submitAction }) {
  const initialValues = {
    name: '',
    sector: 0,
    factories: [],
  }
  const validationSchema = yup.object().shape({
    name: yup.string().required("Name is a required field"),
    sector: yup.string().required("Sector is required"),
  })
  return (<>
    <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={values => {console.log(values)}}
    >
      <AddStationForm cancelAction={cancelAction} submitAction={submitAction} />
    </Formik>
  </>)
}