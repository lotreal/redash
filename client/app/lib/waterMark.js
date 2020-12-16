import React from "react";

import {currentUser} from "@/services/auth";
import ReactWaterMark from 'react-watermark-component';

export default function WaterMark({children}) {
  const beginAlarm = function () {
    console.log('start alarm');
  };
  const options = {
    chunkWidth: 200,
    chunkHeight: 60,
    textAlign: 'left',
    textBaseline: 'bottom',
    globalAlpha: 0.17,
    font: '14px sans-serif',
    rotateAngle: -0.26,
    fillStyle: '#666'
  }

  return <ReactWaterMark
    waterMarkText={currentUser.name}
    openSecurityDefense
    securityAlarm={beginAlarm}
    options={options}
  >
    {children}
  </ReactWaterMark>
}
