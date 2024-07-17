## Cale 7 color WiFi download BMP example

This will download a WiFi URL that should deliver a BMP image (Either 4 bit or 24 bit-depth)

For that we recomment using [CALE image service at cale.es](https://cale.es) where you can add an Image gallery to your desired screen and will create an URL for you. 

Please do not forget to run:

    pio run -t menuconfig

in order to configure your WiFi connection plus the desired URL. If you want to make your BMP private there is also an optional Bearer Token that you can copy from **cale.es**
If that token does not match the one that is entered in menuconfig then the download will not take place.

(Top) → CALE Configuration

