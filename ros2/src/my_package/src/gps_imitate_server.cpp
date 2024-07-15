#include <rclcpp/rclcpp.hpp>
#include <jsoncpp/json/json.h>
#include <boost/asio.hpp>

using boost::asio::ip::tcp;

class GPSImitateServer : public rclcpp::Node {
public:
    GPSImitateServer() : Node("gps_imitate_server") {
        // Setup TCP server
        tcp::acceptor acceptor(io_context, tcp::endpoint(tcp::v4(), 8080));

        // Accept incoming connection
        tcp::socket socket(io_context);
        acceptor.accept(socket);

        // Pack data into JSON format
        Json::Value data;
        data["instruct"] = "gps-imitate-instruct";
        data["longitude"] = 112.0;
        data["latitude"] = 23.55;
        data["direction"] = 90.0;
        data["speed"] = 3;

        // Convert JSON to string
        std::string jsonStr = data.toStyledString();

        // Send JSON data over TCP connection
        boost::asio::write(socket, boost::asio::buffer(jsonStr));
    }

private:
    boost::asio::io_context io_context;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<GPSImitateServer>());
    rclcpp::shutdown();
    return 0;
}


// 客户端
// #include <iostream>
// #include <jsoncpp/json/json.h>
// #include <boost/asio.hpp>

// using boost::asio::ip::tcp;

// int main() {
//     try {
//         boost::asio::io_context io_context;
//         tcp::socket socket(io_context);
//         tcp::resolver resolver(io_context);
//         boost::asio::connect(socket, resolver.resolve({"127.0.0.1", "8080"}));

//         while (true) {
//             // Receive JSON data
//             boost::asio::streambuf buf;
//             boost::asio::read_until(socket, buf, "\n");
//             std::istream input_stream(&buf);
//             std::string jsonStr;
//             std::getline(input_stream, jsonStr);

//             // Parse JSON data
//             Json::Value data;
//             Json::Reader reader;
//             if (reader.parse(jsonStr, data)) {
//                 double longitude = data["longitude"].asDouble();
//                 double latitude = data["latitude"].asDouble();
//                 std::cout << "Received data - Longitude: " << longitude << ", Latitude: " << latitude << std::endl;
//             }
//         }
//     } catch (std::exception& e) {
//         std::cerr << e.what() << std::endl;
//     }

//     return 0;
// }
