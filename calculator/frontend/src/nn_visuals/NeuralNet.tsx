
// @ts-ignore
// import NNVisualizer from 'neural-network-visualizer';
import NNVisualizer from '/src/nn_visuals/NNVisualiser.js'; // ✅ Works with default exports
import { useEffect } from 'react';

export interface Layer {
  units: number;
  fill?: string[]; // Optional array of colours
  stroke?: string; // Optional stroke colour
  strokeWidth?: number; // Optional stroke width
  radius?: number; // Optional radius
}
export type LayersConfig = Layer[];


export default function NeuralNet({ layersRepresentation }: { layersRepresentation: LayersConfig }) {
  
    useEffect(() => {
        const target = document.getElementById("visualizer-container");
        if (target  && !target.hasChildNodes()) {
            new NNVisualizer(target, {
                width: 800,
                height: 600,
                network: {
                    layers:layersRepresentation,
                    diameter: 20
                },
            });
        }
    }, []);

    return <div id="visualizer-container"></div>;
}

// export default function NeuralNet(){

//     return (
//         <div>
//             <NNVisualizer
//     width={800}
//     height={600}
//     lineColor="black"
//     lineWidth="5"
//     network={{
//       vertical: false,
//       layers: [
//         {
//           units: 3,
//         },
//         {
//           units: 4,
//           fill: 'red',
//           stroke: 'black',
//           strokeWidth: 10,
//           radius: 30,
//         },
//         {
//           units: 2,
//         },
//       ],
//     }}
//   />
//         </div>
//      );
// }