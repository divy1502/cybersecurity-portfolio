import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.160.1/build/three.module.js";

const canvas = document.getElementById("cyber-world");
const hero = document.querySelector(".hero");

if (canvas && hero) {
  const reducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;

  try {
    const renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: true,
      antialias: true,
      powerPreference: "high-performance",
    });

    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
    renderer.outputColorSpace = THREE.SRGBColorSpace;

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0b0f14, 0.035);

    const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
    camera.position.set(0, 1, 11);

    const world = new THREE.Group();
    world.position.set(2.4, 0, 0);
    scene.add(world);

    // Cinematic lighting
    scene.add(new THREE.AmbientLight(0x6fb1ff, 0.45));

    const amberLight = new THREE.PointLight(0xffb454, 90, 22);
    amberLight.position.set(4, 4, 5);
    scene.add(amberLight);

    const blueLight = new THREE.PointLight(0x6fb1ff, 55, 22);
    blueLight.position.set(-4, -2, -5);
    scene.add(blueLight);

    // A cluster of futuristic server towers
    const towerMaterial = new THREE.MeshStandardMaterial({
      color: 0x151d2a,
      metalness: 0.78,
      roughness: 0.28,
    });

    const edgeMaterial = new THREE.LineBasicMaterial({
      color: 0x536b86,
      transparent: true,
      opacity: 0.35,
    });

    const signalMaterial = new THREE.MeshBasicMaterial({
      color: 0xffb454,
      toneMapped: false,
    });

    for (let i = 0; i < 13; i++) {
      const angle = (i / 13) * Math.PI * 2;
      const radius = 2.6 + (i % 3) * 0.65;
      const height = 2.5 + (i % 4) * 0.65;

      const tower = new THREE.Group();
      tower.position.set(
        Math.cos(angle) * radius,
        -1,
        Math.sin(angle) * radius - 2,
      );

      const geometry = new THREE.BoxGeometry(0.65, height, 0.85);
      const mesh = new THREE.Mesh(geometry, towerMaterial);
      tower.add(mesh);

      const edges = new THREE.LineSegments(
        new THREE.EdgesGeometry(geometry),
        edgeMaterial,
      );
      tower.add(edges);

      // Illuminated horizontal server indicators
      for (let j = 0; j < 5; j++) {
        const indicator = new THREE.Mesh(
          new THREE.BoxGeometry(0.35, 0.025, 0.012),
          signalMaterial,
        );
        indicator.position.set(0, -height / 2 + 0.4 + j * 0.3, 0.438);
        tower.add(indicator);
      }

      world.add(tower);
    }

    // Central rotating cyber-energy rings
    const ringGroup = new THREE.Group();
    ringGroup.position.set(0, 0.3, -1);
    world.add(ringGroup);

    const ringColors = [0xffb454, 0x6fb1ff, 0xffd08a];

    for (let i = 0; i < 3; i++) {
      const geometry = new THREE.TorusGeometry(1.25 + i * 0.37, 0.018, 8, 120);

      const material = new THREE.MeshBasicMaterial({
        color: ringColors[i],
        transparent: true,
        opacity: 0.7,
      });

      const ring = new THREE.Mesh(geometry, material);
      ring.rotation.x = i * 0.42;
      ring.rotation.y = i * 0.75;
      ringGroup.add(ring);
    }

    // Floating data particles
    const particleCount = 260;
    const positions = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 18;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 12;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 16 - 3;
    }

    const particleGeometry = new THREE.BufferGeometry();
    particleGeometry.setAttribute(
      "position",
      new THREE.BufferAttribute(positions, 3),
    );

    const particles = new THREE.Points(
      particleGeometry,
      new THREE.PointsMaterial({
        color: 0xffb454,
        size: 0.035,
        transparent: true,
        opacity: 0.65,
        sizeAttenuation: true,
      }),
    );
    scene.add(particles);

    let scrollProgress = 0;
    let mouseX = 0;
    let mouseY = 0;
    let visible = true;
    let running = true;

    function resize() {
      const width = Math.max(hero.clientWidth, 1);
      const height = Math.max(hero.clientHeight, 1);

      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();

      // More room for readable text on smaller screens
      world.position.x = width < 700 ? 0.4 : 2.4;
    }

    function updateScroll() {
      const rect = hero.getBoundingClientRect();
      const travel = Math.max(hero.offsetHeight, 1);
      scrollProgress = THREE.MathUtils.clamp(-rect.top / travel, 0, 1);
    }

    window.addEventListener("scroll", updateScroll, { passive: true });

    window.addEventListener(
      "pointermove",
      (event) => {
        mouseX = (event.clientX / window.innerWidth - 0.5) * 2;
        mouseY = (event.clientY / window.innerHeight - 0.5) * 2;
      },
      { passive: true },
    );

    const observer = new IntersectionObserver((entries) => {
      visible = entries[0].isIntersecting;
    });
    observer.observe(hero);

    const resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(hero);

    const clock = new THREE.Clock();

    function animate() {
      if (!running) return;
      requestAnimationFrame(animate);

      if (!visible || document.hidden) {
        clock.getDelta();
        return;
      }

      const time = clock.getElapsedTime();

      if (!reducedMotion) {
        ringGroup.rotation.y = time * 0.15;
        ringGroup.rotation.z = Math.sin(time * 0.25) * 0.1;
        particles.rotation.y = time * 0.008;
      }

      const targetZ = 11 - scrollProgress * 3.5;
      const targetX = reducedMotion ? 0 : mouseX * 0.35;
      const targetY = reducedMotion ? 1 : 1 - mouseY * 0.2;

      camera.position.z += (targetZ - camera.position.z) * 0.055;
      camera.position.x += (targetX - camera.position.x) * 0.055;
      camera.position.y += (targetY - camera.position.y) * 0.055;
      camera.lookAt(0.7, 0, -2);

      renderer.render(scene, camera);
    }

    resize();
    updateScroll();
    animate();

    // Release GPU resources when leaving the page
    window.addEventListener(
      "pagehide",
      () => {
        running = false;
        observer.disconnect();
        resizeObserver.disconnect();
        scene.traverse((object) => {
          if (object.geometry) object.geometry.dispose();
        });
        renderer.dispose();
      },
      { once: true },
    );
  } catch (error) {
    console.warn("3D experience unavailable:", error);
    canvas.style.display = "none";
  }
}
