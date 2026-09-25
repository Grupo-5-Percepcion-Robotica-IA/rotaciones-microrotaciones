#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Vector3


class RotacionROS(Node):

    def __init__(self):
        super().__init__('rotacion_pc')

        self.publisher = self.create_publisher(
            Float64MultiArray,
            '/rotacion_entrada',
            10
        )

        self.sub_directo = self.create_subscription(
            Vector3,
            '/vector_directo',
            self.callback_directo,
            10
        )

        self.sub_micro = self.create_subscription(
            Vector3,
            '/vector_micro',
            self.callback_micro,
            10
        )

        self.recibido_directo = False
        self.recibido_micro = False

    def callback_directo(self, msg):
        print("\nROTACIÓN DIRECTA")
        print(f"x = {msg.x:.6f}")
        print(f"y = {msg.y:.6f}")
        print(f"z = {msg.z:.6f}")
        self.recibido_directo = True

    def callback_micro(self, msg):
        print("\nMICRORROTACIÓN")
        print(f"x = {msg.x:.6f}")
        print(f"y = {msg.y:.6f}")
        print(f"z = {msg.z:.6f}")
        self.recibido_micro = True

    def enviar_rotacion(self):

        print("\n=== DATOS DE ROTACIÓN ===")

        vx = float(input("Vector X: "))
        vy = float(input("Vector Y: "))
        vz = float(input("Vector Z: "))

        nx = float(input("Eje nx: "))
        ny = float(input("Eje ny: "))
        nz = float(input("Eje nz: "))

        angulo = float(input("Ángulo [grados]: "))
        N = float(input("Cantidad de microrrotaciones N: "))

        msg = Float64MultiArray()

        msg.data = [
            vx, vy, vz,
            nx, ny, nz,
            angulo,
            N
        ]

        print("\nEnviando:")
        print(msg.data)

        self.publisher.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    nodo = RotacionROS()

    # Esperar un momento para que ROS descubra el publisher
    rclpy.spin_once(nodo, timeout_sec=1.0)

    nodo.enviar_rotacion()

    print("\nEsperando resultados del ESP32...\n")

    while rclpy.ok():

        rclpy.spin_once(nodo, timeout_sec=0.1)

        if nodo.recibido_directo and nodo.recibido_micro:
            break

    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()