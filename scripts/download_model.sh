echo "$(ls)"
MODEL_PATH="https://github.com/CVHub520/X-AnyLabeling/releases/download/v1.0.0/groundingdino_swint_ogc_quant.onnx"
DEST_DIR="models" # The default destination is /models, but it should be set to /app/model when building docker image

# mkdir -p $DEST_DIR

echo "Starting model download script to $DEST_DIR"
curl -L $MODEL_PATH -o $DEST_DIR/groundingdino_swint_ogc_quant.onnx
echo "File downloaded to $DEST_DIR/groundingdino_swint_ogc_quant.onnx"