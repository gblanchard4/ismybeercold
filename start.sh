python3 src/ismybeercold.py &
cd /etc/node_exporter-$NODE_EXPORTER_VERSION.$DIST_ARCH \
  && ./node_exporter --web.listen-address=":9090" --web.telemetry-path="/metrics"
