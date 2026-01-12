import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '0ca'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '16f'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '9b9'),
            routes: [
              {
                path: '/docs/assessments/',
                component: ComponentCreator('/docs/assessments/', '373'),
                exact: true
              },
              {
                path: '/docs/assessments/gazebo-robot-project',
                component: ComponentCreator('/docs/assessments/gazebo-robot-project', '4a1'),
                exact: true
              },
              {
                path: '/docs/assessments/ros2-basics-quiz',
                component: ComponentCreator('/docs/assessments/ros2-basics-quiz', '22c'),
                exact: true
              },
              {
                path: '/docs/assessments/vla-capstone',
                component: ComponentCreator('/docs/assessments/vla-capstone', '97d'),
                exact: true
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '61d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/learning-paths/',
                component: ComponentCreator('/docs/learning-paths/', '2fa'),
                exact: true
              },
              {
                path: '/docs/learning-paths/complete-physical-ai',
                component: ComponentCreator('/docs/learning-paths/complete-physical-ai', 'bb7'),
                exact: true
              },
              {
                path: '/docs/learning-paths/quick-start',
                component: ComponentCreator('/docs/learning-paths/quick-start', '088'),
                exact: true
              },
              {
                path: '/docs/learning-paths/robotics-foundations',
                component: ComponentCreator('/docs/learning-paths/robotics-foundations', '60c'),
                exact: true
              },
              {
                path: '/docs/learning-paths/simulation-specialist',
                component: ComponentCreator('/docs/learning-paths/simulation-specialist', '695'),
                exact: true
              },
              {
                path: '/docs/learning-paths/software-developer',
                component: ComponentCreator('/docs/learning-paths/software-developer', '112'),
                exact: true
              },
              {
                path: '/docs/module-1/',
                component: ComponentCreator('/docs/module-1/', '8e0'),
                exact: true
              },
              {
                path: '/docs/module-1/ch1-1',
                component: ComponentCreator('/docs/module-1/ch1-1', '8a2'),
                exact: true
              },
              {
                path: '/docs/module-1/ch1-2',
                component: ComponentCreator('/docs/module-1/ch1-2', '8c6'),
                exact: true
              },
              {
                path: '/docs/module-1/ch1-3',
                component: ComponentCreator('/docs/module-1/ch1-3', '906'),
                exact: true
              },
              {
                path: '/docs/module-1/ch1-4',
                component: ComponentCreator('/docs/module-1/ch1-4', '641'),
                exact: true
              },
              {
                path: '/docs/module-2/',
                component: ComponentCreator('/docs/module-2/', 'e75'),
                exact: true
              },
              {
                path: '/docs/module-2/ch2-1',
                component: ComponentCreator('/docs/module-2/ch2-1', '5af'),
                exact: true
              },
              {
                path: '/docs/module-2/ch2-2',
                component: ComponentCreator('/docs/module-2/ch2-2', '2da'),
                exact: true
              },
              {
                path: '/docs/module-2/ch2-3',
                component: ComponentCreator('/docs/module-2/ch2-3', '73b'),
                exact: true
              },
              {
                path: '/docs/module-2/ch2-4',
                component: ComponentCreator('/docs/module-2/ch2-4', '1d0'),
                exact: true
              },
              {
                path: '/docs/module-3/',
                component: ComponentCreator('/docs/module-3/', '127'),
                exact: true
              },
              {
                path: '/docs/module-3/ch3-1',
                component: ComponentCreator('/docs/module-3/ch3-1', '81e'),
                exact: true
              },
              {
                path: '/docs/module-3/ch3-2',
                component: ComponentCreator('/docs/module-3/ch3-2', '450'),
                exact: true
              },
              {
                path: '/docs/module-3/ch3-3',
                component: ComponentCreator('/docs/module-3/ch3-3', '6cc'),
                exact: true
              },
              {
                path: '/docs/module-3/ch3-4',
                component: ComponentCreator('/docs/module-3/ch3-4', '858'),
                exact: true
              },
              {
                path: '/docs/module-4/',
                component: ComponentCreator('/docs/module-4/', '710'),
                exact: true
              },
              {
                path: '/docs/module-4/ch4-1',
                component: ComponentCreator('/docs/module-4/ch4-1', 'e70'),
                exact: true
              },
              {
                path: '/docs/module-4/ch4-2',
                component: ComponentCreator('/docs/module-4/ch4-2', '6bf'),
                exact: true
              },
              {
                path: '/docs/module-4/ch4-3',
                component: ComponentCreator('/docs/module-4/ch4-3', 'bc4'),
                exact: true
              },
              {
                path: '/docs/module-4/ch4-4',
                component: ComponentCreator('/docs/module-4/ch4-4', 'f1d'),
                exact: true
              },
              {
                path: '/docs/part1-foundations/chapter-1-intro',
                component: ComponentCreator('/docs/part1-foundations/chapter-1-intro', '955'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/part1-foundations/chapter-2-ros2',
                component: ComponentCreator('/docs/part1-foundations/chapter-2-ros2', 'b47'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/part2-simulation/chapter-3-urdf',
                component: ComponentCreator('/docs/part2-simulation/chapter-3-urdf', '828'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/part2-simulation/chapter-4-gazebo',
                component: ComponentCreator('/docs/part2-simulation/chapter-4-gazebo', '644'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/part2-simulation/chapter-5-isaac',
                component: ComponentCreator('/docs/part2-simulation/chapter-5-isaac', 'dd2'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/part3-perception/chapter-6-vision',
                component: ComponentCreator('/docs/part3-perception/chapter-6-vision', '4e7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/part3-perception/chapter-7-slam',
                component: ComponentCreator('/docs/part3-perception/chapter-7-slam', '103'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/part4-ai-integration/chapter-8-vla',
                component: ComponentCreator('/docs/part4-ai-integration/chapter-8-vla', '97b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/part4-ai-integration/chapter-9-rl',
                component: ComponentCreator('/docs/part4-ai-integration/chapter-9-rl', '56a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/part5-humanoid-dev/chapter-10-kinematics',
                component: ComponentCreator('/docs/part5-humanoid-dev/chapter-10-kinematics', 'f17'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/part5-humanoid-dev/chapter-11-hri',
                component: ComponentCreator('/docs/part5-humanoid-dev/chapter-11-hri', 'ecc'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/part5-humanoid-dev/chapter-12-capstone',
                component: ComponentCreator('/docs/part5-humanoid-dev/chapter-12-capstone', '08d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/toc',
                component: ComponentCreator('/docs/toc', '6af'),
                exact: true
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '2e1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
