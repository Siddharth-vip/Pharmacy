/**
 * MedicoMart - Interactive 3D Healthcare Hero & WebGL Experience
 * Lightweight, performant Three.js implementation for Django Templates
 */

(function () {
  'use strict';

  // Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initHero3D() {
    const container = document.getElementById('hero-3d-container');
    const canvas = document.getElementById('hero-3d-canvas');
    if (!container || !canvas || typeof THREE === 'undefined') return;

    const width = container.clientWidth;
    const height = container.clientHeight || 500;

    // 1. Scene & Camera Setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 1000);
    camera.position.set(0, 0.4, 7.5);

    // 2. WebGL Renderer with Alpha & Antialiasing
    const renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance'
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    if (renderer.outputEncoding) {
      renderer.outputEncoding = THREE.sRGBEncoding;
    }

    // 3. Lighting Setup
    const ambientLight = new THREE.AmbientLight(0xfaf7f0, 0.9);
    scene.add(ambientLight);

    const mainLight = new THREE.DirectionalLight(0x1a8f6b, 1.4);
    mainLight.position.set(5, 8, 6);
    scene.add(mainLight);

    const goldPointLight = new THREE.PointLight(0xc9b27c, 1.6, 20);
    goldPointLight.position.set(-4, -2, 4);
    scene.add(goldPointLight);

    const rimLight = new THREE.DirectionalLight(0x123f35, 0.8);
    rimLight.position.set(-6, 4, -4);
    scene.add(rimLight);

    // 4. Main 3D Group
    const rootGroup = new THREE.Group();
    scene.add(rootGroup);

    // --- A. Medicine Bottle Mesh ---
    const bottleGroup = new THREE.Group();

    // Bottle Body
    const bottleBodyGeo = new THREE.CylinderGeometry(1.0, 1.05, 2.4, 32);
    const bottleMat = new THREE.MeshPhysicalMaterial({
      color: 0x123f35,
      emissive: 0x071b16,
      roughness: 0.18,
      metalness: 0.1,
      transmission: 0.65,
      ior: 1.45,
      transparent: true,
      opacity: 0.92,
      reflectivity: 0.9
    });
    const bottleBody = new THREE.Mesh(bottleBodyGeo, bottleMat);
    bottleBody.position.y = 0;
    bottleGroup.add(bottleBody);

    // Bottle Shoulder
    const shoulderGeo = new THREE.CylinderGeometry(0.65, 1.0, 0.4, 32);
    const bottleShoulder = new THREE.Mesh(shoulderGeo, bottleMat);
    bottleShoulder.position.y = 1.4;
    bottleGroup.add(bottleShoulder);

    // Bottle Neck
    const neckGeo = new THREE.CylinderGeometry(0.55, 0.65, 0.45, 32);
    const bottleNeck = new THREE.Mesh(neckGeo, bottleMat);
    bottleNeck.position.y = 1.75;
    bottleGroup.add(bottleNeck);

    // Bottle Cap (Gold / Beige Ribbed Finish)
    const capGeo = new THREE.CylinderGeometry(0.6, 0.6, 0.45, 32);
    const capMat = new THREE.MeshStandardMaterial({
      color: 0xc9b27c,
      roughness: 0.3,
      metalness: 0.8
    });
    const bottleCap = new THREE.Mesh(capGeo, capMat);
    bottleCap.position.y = 2.1;
    bottleGroup.add(bottleCap);

    // Bottle Label Wrap
    const labelGeo = new THREE.CylinderGeometry(1.02, 1.07, 1.5, 32, 1, true, -Math.PI * 0.7, Math.PI * 1.4);
    const labelMat = new THREE.MeshStandardMaterial({
      color: 0xfcfaf5,
      roughness: 0.6,
      metalness: 0.05,
      side: THREE.DoubleSide
    });
    const labelMesh = new THREE.Mesh(labelGeo, labelMat);
    labelMesh.position.y = -0.1;
    bottleGroup.add(labelMesh);

    // Cross on Label
    const crossMat = new THREE.MeshStandardMaterial({
      color: 0x1a8f6b,
      roughness: 0.2,
      metalness: 0.3
    });
    const crossV = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.4, 0.04), crossMat);
    crossV.position.set(0, -0.1, 1.06);
    bottleGroup.add(crossV);

    const crossH = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.12, 0.04), crossMat);
    crossH.position.set(0, -0.1, 1.06);
    bottleGroup.add(crossH);

    bottleGroup.position.set(0.2, 0, 0);
    bottleGroup.rotation.y = 0.35;
    rootGroup.add(bottleGroup);

    // --- B. Floating Vitamin Capsules ---
    const capsules = [];
    const capsuleMatGreen = new THREE.MeshStandardMaterial({
      color: 0x123f35,
      roughness: 0.25,
      metalness: 0.3
    });
    const capsuleMatGold = new THREE.MeshStandardMaterial({
      color: 0xc9b27c,
      roughness: 0.2,
      metalness: 0.65
    });
    const capsuleMatWhite = new THREE.MeshStandardMaterial({
      color: 0xfcfaf5,
      roughness: 0.25,
      metalness: 0.1
    });

    function createCapsule(color1Mat, color2Mat) {
      const capGroup = new THREE.Group();
      const radius = 0.24;
      const height = 0.45;

      // Top Half
      const topCyl = new THREE.CylinderGeometry(radius, radius, height / 2, 24);
      const topMesh = new THREE.Mesh(topCyl, color1Mat);
      topMesh.position.y = height / 4;
      capGroup.add(topMesh);

      const topSphere = new THREE.Mesh(new THREE.SphereGeometry(radius, 24, 16, 0, Math.PI * 2, 0, Math.PI / 2), color1Mat);
      topSphere.position.y = height / 2;
      capGroup.add(topSphere);

      // Bottom Half
      const botCyl = new THREE.CylinderGeometry(radius, radius, height / 2, 24);
      const botMesh = new THREE.Mesh(botCyl, color2Mat);
      botMesh.position.y = -height / 4;
      capGroup.add(botMesh);

      const botSphere = new THREE.Mesh(new THREE.SphereGeometry(radius, 24, 16, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), color2Mat);
      botSphere.position.y = -height / 2;
      capGroup.add(botSphere);

      return capGroup;
    }

    const capsule1 = createCapsule(capsuleMatGreen, capsuleMatGold);
    capsule1.position.set(-2.2, 1.4, 0.8);
    capsule1.rotation.set(0.6, 0.4, 0.9);
    rootGroup.add(capsule1);
    capsules.push({ mesh: capsule1, speed: 0.015, radius: 2.3, offset: 0 });

    const capsule2 = createCapsule(capsuleMatGold, capsuleMatWhite);
    capsule2.position.set(2.4, -0.8, 1.0);
    capsule2.rotation.set(-0.5, 0.8, -0.6);
    rootGroup.add(capsule2);
    capsules.push({ mesh: capsule2, speed: 0.012, radius: 2.5, offset: 2.1 });

    const capsule3 = createCapsule(capsuleMatGreen, capsuleMatWhite);
    capsule3.position.set(-1.8, -1.6, -0.5);
    capsule3.rotation.set(1.1, -0.3, 0.4);
    rootGroup.add(capsule3);
    capsules.push({ mesh: capsule3, speed: 0.018, radius: 2.0, offset: 4.2 });

    // --- C. Floating Glass Spheres ---
    const sphereMat = new THREE.MeshPhysicalMaterial({
      color: 0xe5d5b8,
      roughness: 0.1,
      transmission: 0.88,
      transparent: true,
      opacity: 0.75,
      ior: 1.33
    });

    const spheres = [];
    const sphere1 = new THREE.Mesh(new THREE.SphereGeometry(0.45, 32, 32), sphereMat);
    sphere1.position.set(2.0, 1.8, -0.8);
    rootGroup.add(sphere1);
    spheres.push({ mesh: sphere1, baseY: 1.8, speed: 0.02, amp: 0.15 });

    const sphere2 = new THREE.Mesh(new THREE.SphereGeometry(0.3, 32, 32), sphereMat);
    sphere2.position.set(-2.5, -0.2, 0.5);
    rootGroup.add(sphere2);
    spheres.push({ mesh: sphere2, baseY: -0.2, speed: 0.025, amp: 0.12 });

    // --- D. Floating Particle Cloud ---
    const particleCount = 120;
    const particleGeo = new THREE.BufferGeometry();
    const particlePos = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount * 3; i += 3) {
      particlePos[i] = (Math.random() - 0.5) * 8.5;
      particlePos[i + 1] = (Math.random() - 0.5) * 6.5;
      particlePos[i + 2] = (Math.random() - 0.5) * 4.5;
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));

    const particleMat = new THREE.PointsMaterial({
      color: 0xc9b27c,
      size: 0.055,
      transparent: true,
      opacity: 0.65,
      blending: THREE.AdditiveBlending
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    rootGroup.add(particles);

    // 5. Mouse Interaction & Parallax Lerp
    let mouseX = 0;
    let mouseY = 0;
    let targetRotX = 0;
    let targetRotY = 0;
    let isVisible = true;

    function onMouseMove(e) {
      const rect = container.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      mouseX = x * 2;
      mouseY = y * 2;
      targetRotY = mouseX * 0.45;
      targetRotX = mouseY * 0.3;
    }

    if (!prefersReducedMotion) {
      window.addEventListener('mousemove', onMouseMove, { passive: true });
    }

    // 6. Responsive Resize Handling
    function handleResize() {
      if (!container || !renderer || !camera) return;
      const w = container.clientWidth;
      const h = container.clientHeight || 500;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    }
    window.addEventListener('resize', handleResize);

    // 7. IntersectionObserver to Pause Render Loop when Offscreen
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        isVisible = entry.isIntersecting;
      });
    }, { threshold: 0.05 });
    observer.observe(container);

    // 8. Animation Render Loop
    let clock = new THREE.Clock();

    function animate() {
      requestAnimationFrame(animate);

      if (!isVisible) return;

      const delta = clock.getDelta();
      const elapsed = clock.getElapsedTime();

      if (!prefersReducedMotion) {
        // Smooth rotation damping
        rootGroup.rotation.y += (targetRotY - rootGroup.rotation.y) * 0.05;
        rootGroup.rotation.x += (targetRotX - rootGroup.rotation.x) * 0.05;

        // Continuous gentle bottle hover & self rotation
        bottleGroup.rotation.y += 0.005;
        bottleGroup.position.y = Math.sin(elapsed * 1.5) * 0.12;

        // Orbit capsules
        capsules.forEach((item, index) => {
          const t = elapsed * item.speed * 20 + item.offset;
          item.mesh.position.y += Math.sin(t) * 0.0025;
          item.mesh.rotation.x += 0.008;
          item.mesh.rotation.y += 0.012;
        });

        // Float spheres
        spheres.forEach((s) => {
          s.mesh.position.y = s.baseY + Math.sin(elapsed * s.speed * 40) * s.amp;
        });

        // Rotate particles slowly
        particles.rotation.y = elapsed * 0.03;
      }

      renderer.render(scene, camera);
    }

    animate();
  }

  // Card 3D Tilt Interaction
  function init3DCardTilt() {
    if (prefersReducedMotion) return;

    const cards = document.querySelectorAll('.card-3d-tilt');
    cards.forEach((card) => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -9;
        const rotateY = ((x - centerX) / centerX) * 9;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
      });
    });
  }

  // Scroll Reveal Observer
  function initScrollAnimations() {
    const revealEls = document.querySelectorAll('.reveal-on-scroll');
    if (!revealEls.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    revealEls.forEach((el) => observer.observe(el));
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initHero3D();
      init3DCardTilt();
      initScrollAnimations();
    });
  } else {
    initHero3D();
    init3DCardTilt();
    initScrollAnimations();
  }
})();
