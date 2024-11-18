./build/lenia -i LeniaConfig.json -o output/output -v
python3 ./src/frameconverter.py -i output/output -o output/video --output_type "mp4" --output_framerate 120 -v