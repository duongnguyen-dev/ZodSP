import os
import onnx
import onnxruntime as ort

class OnnxBaseModel:
    def __init__(self, model_path, device_type: str = "cpu"):
        self.sess_options = ort.SessionOptions()

        if "OMP_NUM_THREADS" in os.environ:
            self.sess_options.inter_op_num_threads = int(
                os.environ["OMP_NUM_THREADS"]
            )

        self.providers = ["CPUExecutionProvider"]
        if device_type.lower() == "gpu":
            self.providers = ["CUDAExecutionProvider"]

        self.ort_sessions = ort.InferenceSession(
            model_path,
            providers=self.providers,
            sess_options=self.sess_options,
        )

        self.model_path = model_path
    
    def get_ort_inference(
        self, blob, inputs=None, extract=True, squeeze=False
    ):
        if inputs is None:
            inputs = self.get_input_name()
            outs = self.ort_sessions.run(None, {inputs: blob})
        else:
            outs = self.ort_sessions.run(None, inputs)
        if extract:
            outs = outs[0]
        if squeeze:
            outs = outs.squeeze(axis=0)
        return outs
    
    def get_input_name(self):
        return self.ort_session.get_inputs()[0].name